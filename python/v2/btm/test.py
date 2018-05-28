from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Storage import *
from boa.builtins import concat
from hons.nep5 import *
from hons.token import *
from hons.arrayUtil import *
from hons.serialization import *

#
NS_REGISTER_FEE = 10 * 100_000_000  # 10 to owners * 10^8
NS_TRANSFER_FEE = 5 * 100_000_000   # 5 to owners * 10^8
NS_STORAGE_PREFIX = 'NAMESERVICE'

def handle_name_service(ctx, operation, args):

    # retreive the address associated with a given name
    # anyone can call
    if operation == 'nameServiceQuery':
        return query(ctx, args[0])

    # retreive a list of names associated with this address
    # anyone can call
    # output: array as bytearray
    elif operation == 'nameServiceQueryAddress':
        return queryAddress(ctx, args[0])

    # remove a link between a given name and it's address
    # can only be called by name owner
    elif operation == 'nameServiceUnregister':
        return unregister(ctx, args[0])

    # create a name to address association for a small fee
    # can only be called by owner of address being registered
    elif operation == 'nameServiceRegister':
        return register(ctx, args[0], args[1])

    # # transfer of a name from owner to a new address
    # # needs to be called twice, once by owner, and once by requester
    # # first one to call creates transfer agreement
    # # secong one to call finalizes transfer agreement, and transfer is executed
    # # if both parties to not fulfil agreement, transfer will not take place

    elif operation == 'nameServicePreApproveTransfer':
        return preApproveTransfer(ctx, args[0], args[1], args[2])

    elif operation == 'nameServiceRequestTransfer':
        return requestTransfer(ctx, args[0], args[1], args[2])

    # SALE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elif operation == 'nameServiceQueryForSale':
        return queryForSale(ctx, args[0])

    elif operation == 'nameServicePostForSale':
        return postForSale(ctx, args[0], args[1])

    elif operation == 'nameServiceCancelForSale':
        return cancelForSale(ctx, args[0])

    elif operation == 'nameServiceAcceptSale':
        return acceptSale(ctx, args[0], args[1])

    # OFFER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    elif operation == 'nameServicePostOffer':
        return postOffer(ctx, args[0], args[1], args[2])

    elif operation == 'nameServiceCancelOffer':
        return cancelOffer(ctx, args[0], args[1])

    elif operation == 'nameServiceFindOffers':
        return findOffers(ctx, args[0])

    elif operation == 'nameServiceGetOffer':
        return getOffer(ctx, args[0], args[1])

    elif operation == 'nameServiceAcceptOffer':
        return acceptOffer(ctx, args[0], args[1])

    return False

def query(ctx, name):
    return getName(ctx, name)


def queryAddress(ctx, address):
    return getName(ctx, address)


def unregister(ctx, name):
    ownerAddress = getName(ctx, name)
    isOwnerAddress = CheckWitness(ownerAddress)

    if ownerAddress == b'':
        print('unregister; record does not exist')
        return False

    if isOwnerAddress == False:
        print('unregister; caller is not owner of record')
        return False

    checkAndDeleteForSale(ctx, name)
    return ns_do_unregister(ctx, name, ownerAddress)


def register(ctx, name, ownerAddress):
    isOwnerAddress = CheckWitness(ownerAddress)
    currentOwnerAddress = getName(ctx, name)

    if isOwnerAddress == False:
        print('register; contract caller is not same as ownerAddress')
        return False

    if currentOwnerAddress != b'':
        if currentOwnerAddress == ownerAddress:
            print('register; name is already registered to caller address')
        else:
            print('register; name is already registered to another address')
        return False

    print('register; all qualifications are met, about to pay fee')
    feePaid = do_fee_collection(ctx, ownerAddress, NS_REGISTER_FEE)
    print('just paid')

    if feePaid == False:
        print('Insufficient funds to pay registration fee')
        return False

    print('register; fees paid, record registration')
    return ns_do_register(ctx, name, ownerAddress)

def preApproveTransfer(ctx, name, ownerAddress, newOwnerAddress):
    print('preApproveTransfer')

    if ownerAddress == newOwnerAddress:
        print('transfer; ownerAddress and newOwnerAddress are the same')
        return False

    if CheckWitness(ownerAddress) == False:
        print('transfer; contract caller is not same as ownerAddress or newOwnerAddress')
        return False

    currentOwnerAddress = getName(ctx, name)
    if currentOwnerAddress == b'':
        print('transfer; name record is empty, please register instead')
        return False

    if currentOwnerAddress != ownerAddress:
        print('transfer; contract caller is not owner of name record')
        return False

    # if passing concat method more than 2 arguments, it pushes extra item on stack
    approvalRecordKey = concat(name, ownerAddress)
    approvalRecordKey = concat(approvalRecordKey, newOwnerAddress)
    approvalRecordRaw = getName(ctx, approvalRecordKey)

    if approvalRecordRaw == b'':
        print('transfer; no approval record, create one with approval from owner')
        feesCollected = do_fee_collection(ctx, ownerAddress, NS_TRANSFER_FEE)
        if feesCollected:
            valueRaw = [True, False]
            value = serialize_array(valueRaw)
            putName(ctx, approvalRecordKey, value)
            return True
        return False

    print('approvalRecordRaw')
    # [{ownerAddressApproval: boolean}, {newOwnerAddress_approval: boolean}]
    approvalRecord = deserialize_bytearray(approvalRecordRaw)
    print('approvalRecord')
    ownerApproves = approvalRecord[0]
    print('ownerApproves')
    newOwnerApproves = approvalRecord[1]
    print('newOwnerApproves')

    # if not this format, gets error from compiler
    # [I 180307 16:44:24 pytoken:253] Op Not Converted: JUMP_IF_FALSE_OR_POP
    if ownerApproves == True:
        if newOwnerApproves == False:
            print('transfer; owner pre approval already created, but waiting for new owner')
            return False

    # if not this format, gets error from compiler
    # [I 180307 16:44:24 pytoken:253] Op Not Converted: JUMP_IF_FALSE_OR_POP
    if ownerApproves == False:
        if newOwnerApproves == True:
            print('transfer; approval record exists and new owner pre approved transfer; execute transfer')
            feesCollected = do_fee_collection(ctx, ownerAddress, NS_TRANSFER_FEE)
            if feesCollected:
                deleteName(ctx, approvalRecordKey)
                return ns_do_transfer(ctx, name, ownerAddress, newOwnerAddress)
            return False

    return False

def requestTransfer(ctx, name, ownerAddress, newOwnerAddress):
    print('transfer')
    isNewOwnerAddress = CheckWitness(newOwnerAddress)

    if isNewOwnerAddress == False:
        print('transfer; contract caller is not the same as new owner')
        return False

    currentOwnerAddress = getName(ctx, name)

    if currentOwnerAddress == b'':
        print('transfer; name record is empty, please register instead')
        return False

    if currentOwnerAddress != ownerAddress:
        print('transfer; request from owner is not owner of this name')
        return False

    # if passing concat method more than 2 arguments, it pushes extra item on stack
    approvalRecordKey = concat(name, ownerAddress)
    approvalRecordKey = concat(approvalRecordKey, newOwnerAddress)
    approvalRecordRaw = getName(ctx, approvalRecordKey)

    if approvalRecordRaw == b'':
        print('transfer; no approval record, create one with approval from new owner')
        feesCollected = do_fee_collection(ctx, newOwnerAddress, NS_TRANSFER_FEE)
        if feesCollected:
            valueRaw = [False, True]
            value = serialize_array(valueRaw)
            putName(ctx, approvalRecordKey, value)
            return True
        return False

    print('approvalRecordRaw')
    # [{ownerAddressApproval: boolean}, {newOwnerAddress_approval: boolean}]
    approvalRecord = deserialize_bytearray(approvalRecordRaw)
    print('approvalRecord')
    ownerApproves = approvalRecord[0]
    print('ownerApproves')
    newOwnerApproves = approvalRecord[1]
    print('newOwnerApproves')

    # if not this format, gets error from compiler
    # [I 180307 16:44:24 pytoken:253] Op Not Converted: JUMP_IF_FALSE_OR_POP
    if ownerApproves == False:
        if newOwnerApproves == True:
            print('transfer; new owner pre approval already created, but waiting for current owner')
            return False

    # if not this format, gets error from compiler
    # [I 180307 16:44:24 pytoken:253] Op Not Converted: JUMP_IF_FALSE_OR_POP
    if ownerApproves == True:
        if newOwnerApproves == False:
            print('transfer; approval record exists and current owner pre approved transfer; execute transfer')
            feesCollected = do_fee_collection(ctx, newOwnerAddress, NS_TRANSFER_FEE)
            if feesCollected :
                print('feesCollected => do_transfer')
                deleteName(ctx, approvalRecordKey)
                return ns_do_transfer(ctx, name, ownerAddress, newOwnerAddress)

    return False


def queryForSale(ctx, name):
    return getName(ctx, concat('FORSALE', name))


def postForSale(ctx, name, amount):
    print('postForSale')
    ownerAddress = getName(ctx, name)
    isOwnerAddress = CheckWitness(ownerAddress)

    if ownerAddress == b'':
        print('postForSale; record does not exist')
        return False

    if isOwnerAddress == False:
        print('postForSale; caller is not owner of record')
        return False

    if amount > 0:
        putName(ctx, concat('FORSALE', name), amount)

    return True


def cancelForSale(ctx, name):
    print('cancelForSale')
    ownerAddress = getName(ctx, name)
    isOwnerAddress = CheckWitness(ownerAddress)

    if ownerAddress == b'':
        print('cancelForSale; record does not exist')
        return False

    if isOwnerAddress == False:
        print('cancelForSale; caller is not owner of record')
        return False

    checkAndDeleteForSale(ctx, name)
    return True


def acceptSale(ctx, name, newOwnerAccount):
    print('acceptSale')
    ownerAddress = getName(ctx, name)
    forSaleRecord = getName(ctx, concat('FORSALE', name))
    isCallerAddress = CheckWitness(newOwnerAccount)

    if ownerAddress == b'':
        print('acceptSale; name record does not exist')
        return False

    if forSaleRecord == b'':
        print('acceptSale; for sales record does not exist')
        return False

    if isCallerAddress == False:
        print('acceptSale; caller is not same as transfer to')
        return False

    if newOwnerAccount == ownerAddress:
        print('acceptSale; caller already owns this name')
        return False

    accountBalance = Get(ctx, newOwnerAccount)
    requiredBalance = forSaleRecord + NS_REGISTER_FEE
    if requiredBalance <= accountBalance:
        feePaid = do_fee_collection(ctx, newOwnerAccount, NS_REGISTER_FEE)
        saleAmountPaid = do_transfer(ctx, newOwnerAccount, TOKEN_OWNER, forSaleRecord)

        return ns_do_transfer(ctx, name, ownerAddress, newOwnerAccount)

    print('acceptSale; insufficient funds')
    return False

def checkAndDeleteForSale(ctx, name):
    forSaleRecord = getName(ctx, concat('FORSALE', name))

    if forSaleRecord != b'':
        return deleteName(ctx, concat('FORSALE', name))

    return True


def postOffer(ctx, name, amount, newOwnerAddress):
    print('postOffer')

    ownerAddress = getName(ctx, name)
    if ownerAddress == b'':
        print('postOffer; record does not exist')
        return False

    isNewOwnerAddress = CheckWitness(newOwnerAddress)
    if isNewOwnerAddress == False:
        print('postOffer; caller is not same as offer address')
        return False

    if ownerAddress == newOwnerAddress:
        print('postOffer; you already own this name')
        return False

    if amount <= 0:
        print('postOffer; amount needs to be at least 1 HONS')
        return False

    nameConcat = concat(name, newOwnerAddress)
    nameConcat = concat('OFFER', nameConcat)
    currentOffer = getName(ctx, nameConcat)

    if currentOffer == amount:
        print('postOffer; Offer already set at this amount, no update needed')
        return True

    # no offer exists
    # put offer amount into escrow
    # collect transfer fee
    # create offer record
    # append offer key to offers array
    #   TODO: replace once Storage.find is ready
    if currentOffer == b'':
        feePaid = do_fee_collection(ctx, newOwnerAddress, amount + NS_TRANSFER_FEE)
        if not feePaid:
            print('postOffer; Insufficient funds to put offer into escrow + registration fee')
            return False
        putName(ctx, nameConcat, amount)

        offers = getName(ctx, concat('OFFERS', name))
        if offers == b'':
            offers = []
        else:
            offers = deserialize_bytearray(offers)

        offers.append(newOwnerAddress)
        offers = serialize_array(offers)
        putName(ctx, concat('OFFERS', name), offers)

        return True
    # current offer already exists
    # update current offer with new amount
    variance = amount - currentOffer

    # new offer larger than current OFFER
    # add to escrow amount
    # collect transfer fee again
    # update offer record
    if variance > 0:
        feePaid = do_fee_collection(ctx, newOwnerAddress, variance + NS_TRANSFER_FEE)
        if not feePaid:
            print('postOffer; Insufficient funds to update escrow + registration fee')
            return False
        putName(ctx, nameConcat, amount)
        return True
    # new offer is smaller than current offer
    # withdrawl from escrow
    # collect transfer fee again
    # update offer record
    invertVariance = 0 - variance
    refund = invertVariance - NS_TRANSFER_FEE
    # if refund is larger than transfer fee, subtract from refund amount
    # transfer remainder to newOwnerAddress
    if refund > 0:
        feePaid = do_transfer(ctx, TOKEN_OWNER, newOwnerAddress, refund)
        if not feePaid:
            print('postOffer; Insufficient funds to update escrow + registration fee')
            return False
        putName(ctx, nameConcat, amount)
        return True

    # variance amount is less transfer fee, charge new Owner differnce
    if refund < 0:
        invertRefund = 0 - refund
        feePaid = do_fee_collection(ctx, newOwnerAddress, invertRefund)
        if not feePaid:
            print('postOffer; Insufficient funds to update escrow + registration fee')
            return False
        putName(ctx, nameConcat, amount)
        return True
    # variance is same as transfer fee, just update offer
    putName(ctx, nameConcat, amount)
    return True

def cancelOffer(ctx, name, newOwnerAddress):
    print('cancelOffer')

    isNewOwnerAddress = CheckWitness(newOwnerAddress)
    if isNewOwnerAddress == False:
        print('cancelOffer; caller is not same as offer address')
        return False

    nameConcat = concat(name, newOwnerAddress)
    nameConcat = concat('OFFER', nameConcat)
    currentOffer = getName(ctx, nameConcat)

    if currentOffer == b'':
        print('cancelOffer; there is no offer record to cancel')
        return False

    # refund amount from escrow to new owner
    # remove record
    # remove offer from offers collection
    #   TODO: remove this step once Storage.find is avail
    do_transfer(ctx, TOKEN_OWNER, newOwnerAddress, currentOffer)
    deleteName(ctx, nameConcat)

    offers = getName(ctx, concat('OFFERS', name))
    offers = removeItem(offers, newOwnerAddress)

    if offers == []:
        deleteName(ctx, concat('OFFERS', name))
    else:
        offers = serialize_array(offers)
        putName(ctx, concat('OFFERS', name), offers)

    return True

def findOffers(ctx, name):
    print('findOffers')
    return getName(ctx, concat('OFFERS', name))

def getOffer(ctx, name, newOwnerAddress):
    print('getOffer')
    nameConcat = concat(name, newOwnerAddress)
    nameConcat = concat('OFFER', nameConcat)
    return getName(ctx, nameConcat)

def acceptOffer(ctx, name, newOwnerAddress):
    print('acceptOffer')

    ownerAddress = getName(ctx, name)
    if ownerAddress == b'':
        print('acceptOffer; record does not exist')
        return False

    isOwnerAddress = CheckWitness(ownerAddress)
    if isOwnerAddress == False:
        print('acceptOffer; caller is not same as owner address')
        return False

    nameConcat = concat(name, newOwnerAddress)
    nameConcat = concat('OFFER', nameConcat)
    offer = getName(ctx, nameConcat)

    if offer == b'':
        print('acceptOffer; this offer does not exist')
        return False

    # transfer funds from escrow to old owner for amount of offer - trans fee
    if offer > NS_TRANSFER_FEE:
        do_transfer(ctx, TOKEN_OWNER, ownerAddress, offer - NS_TRANSFER_FEE)
    # if trans fee if more than offer, collect fee diff from old owner
    elif offer < NS_TRANSFER_FEE:
        feePaid = do_fee_collection(ctx, ownerAddress, NS_TRANSFER_FEE - offer)
        if not feePaid:
            print('acceptOffer; Insufficient funds for transfer fee')
            return False

    # transfer name
    # delete offer and remove from list
    print('acceptOffer; amount moved from escrow to owner, transfer name')
    nameTransferSuccess = ns_do_transfer(ctx, name, ownerAddress, newOwnerAddress)

    print('acceptOffer; delete offer record')
    deleteName(ctx, nameConcat)

    print('acceptOffer; get offers list for name')
    offers = getName(ctx, concat('OFFERS', name))

    print('acceptOffer; deserialize offers list from storage')
    offers = deserialize_bytearray(offers)

    print('acceptOffer; remove accepted offer from list')
    offers = removeItem(offers, newOwnerAddress)

    if len(offers) == 0:
        print('acceptOffer; delete offer list since none remain')
        result = deleteName(ctx, concat('OFFERS', name))
    else:
        print('acceptOffer; serialize updated offer list')
        offers = serialize_array(offers)
        print('acceptOffer; put updated list back into storage')
        result = putName(ctx, concat('OFFERS', name), offers)

    return True


def do_fee_collection(ctx, address, fee):
    feePaid = do_transfer(ctx, address, TOKEN_OWNER, fee)

    if not feePaid:
        print('Insufficient funds to pay registration fee')
        return False

    print('do_fee_collection; fees paid successfully')
    return True


def ns_do_transfer(ctx, name, ownerAddress, newOwnerAddress):

    checkAndDeleteForSale(ctx, name)

    prevOwnerAddressNameList = getName(ctx, ownerAddress)
    if not prevOwnerAddressNameList:
        print('not possible')
        return False
    else:
        prevOwnerAddressNameList = deserialize_bytearray(prevOwnerAddressNameList)
        newList = removeItem(prevOwnerAddressNameList, name)

    if len(newList) == 0:
        deleteName(ctx, ownerAddress)
        # fails without this print statement?!?!?!
        print('')
    else:
        serializedList = serialize_array(newList)
        putName(ctx, ownerAddress, serializedList)


    print('removed record from prev owner list, about to add to new owner list')
    newOwnerAddressNameList = getName(ctx, newOwnerAddress)
    if newOwnerAddressNameList == b'':
        print('if not addressNameList')
        newOwnerAddressNameList = []
    else:
        newOwnerAddressNameList = deserialize_bytearray(newOwnerAddressNameList)

    newOwnerAddressNameList = addItem(newOwnerAddressNameList, name)
    serializedList = serialize_array(newOwnerAddressNameList)
    putName(ctx, newOwnerAddress, serializedList)


    print('name added to new owner list')
    putName(ctx, name, newOwnerAddress)

    return True


def ns_do_register(ctx, name, newOwnerAddress):
    # get current list of names for ownerAddress
    # append name to list
    # put list back
    # put name -> address record
    print('ns_do_register')
    addressNameList = getName(ctx, newOwnerAddress)
    if addressNameList == b'':
        print('if not addressNameList')
        addressNameList = [name]
    else:
        addressNameList = deserialize_bytearray(addressNameList)
        addressNameList = addItem(addressNameList, name)

    serializedList = serialize_array(addressNameList)
    putName(ctx, newOwnerAddress, serializedList)
    putName(ctx, name, newOwnerAddress)
    return True


def ns_do_unregister(ctx, name, ownerAddress):
    # get current list of names for ownerAddress
    # delete name from list
    # put list back
    # delete name -> address record
    print('ns_do_unregister')
    addressNameList = getName(ctx, ownerAddress)

    if addressNameList == b'':
        print('not possible')
        return False

    else:
        addressNameList = deserialize_bytearray(addressNameList)
        # previously used Array.remove function before python 3.6 neo-boa 0.3.7
        # however does not appear to be working anymore
        # addressNameList = addressNameList.remove(name)
        newList = removeItem(addressNameList, name)

    if len(newList) == 0:
        deleteName(ctx, ownerAddress)
        # fails without this print statement?!?!?!
        print('')
    else:
        serializedList = serialize_array(newList)
        putName(ctx, ownerAddress, serializedList)

    deleteName(ctx, name)
    return True


# def findName(ctx, query):
#     return Find(ctx, prefixStorageKey(query))


def putName(ctx, key, value):
    return Put(ctx, prefixStorageKey(key), value)


def getName(ctx, key):
    return Get(ctx,  prefixStorageKey(key))


def deleteName(ctx, key):
    return Delete(ctx, prefixStorageKey(key))


def prefixStorageKey(key):
return concat(NS_STORAGE_PREFIX, key)