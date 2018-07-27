"""
Varimi :  NEO smart contract 
Author :  Tongayi Choto
Email  :  chototongayi@gmail.com
Date   :  June 14 2018
"""
VERSION = "1.1.0"

# The Main BitMari Smart Farm Contract 
# All other features of the contract will be accesed from this file
# These include the digital coupon and farm contract registration
##  examples invocations according to the above  
##  build /smart-contracts/smart-farm-contracts.py     "hash": "60658df50dea2631719f0beaef6c6b04a4a284a5"
##  import contract /smart-contracts/smart-farm-contracts.avm 0710 05 True False
##         print("Entered Arguments: [FarmContract_name][OwnerNeoAddress][Farmer_id][Buyer_id][Project_id][Contract_id][Balance][Status]")
## testinvoke 8b68b442bb6530a472446b52e3c13c4378a50aca RegisterFarmContract ["Tongayi","AdGqXwm3aNbBgFsXwZdB8aypzFT73ViSmM", "F13","B11","P22","C33","560","Pending","other_data"]
## testinvoke 8b68b442bb6530a472446b52e3c13c4378a50aca QueryFarmContract ["Tongayi","AdGqXwm3aNbBgFsXwZdB8aypzFT73ViSmM"]
## testinvoke 8b68b442bb6530a472446b52e3c13c4378a50aca UnregisterFarmContract ["Tongayi","AdGqXwm3aNbBgFsXwZdB8aypzFT73ViSmM"]
## testinvoke 8b68b442bb6530a472446b52e3c13c4378a50aca UpdateFarmContract ["Tongayi","AdGqXwm3aNbBgFsXwZdB8aypzFT73ViSmM", "F13","B11","P22","C33","510","Pending","other_data"]
## testinvoke 8b68b442bb6530a472446b52e3c13c4378a50aca TransferFarmContract ["Tongayi","AdGqXwm3aNbBgFsXwZdB8aypzFT73ViSmM","AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y"]
## testinvoke 8b68b442bb6530a472446b52e3c13c4378a50aca RateFarmContractParticipant ["AdGqXwm3aNbBgFsXwZdB8aypzFT73ViSmM", 2]
## testinvoke 8b68b442bb6530a472446b52e3c13c4378a50aca GetParticipantRating ["AdGqXwm3aNbBgFsXwZdB8aypzFT73ViSmM"]
## 

# import  neo boa services
from boa.interop.Neo.Runtime import Log, Notify, GetTrigger, CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.TransactionType import InvocationTransaction
from boa.interop.Neo.Transaction import *
from boa.interop.System.ExecutionEngine import InvocationTransaction
from boa.interop.System.ExecutionEngine import GetScriptContainer
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Output import GetScriptHash, GetValue, GetAssetId
from boa.interop.Neo.Storage import Get, Put,Delete, GetContext
from boa.builtins import concat

# import btm points 
# from btm.txio import get_asset_attachments
# from btm.token import *
# from btm.crowdsale import *
# from btm.nep5 import *
# from btm.arrayUtil import *
from btm.serialization import *

# import other agriculture contracts
#from btm.rating import *


# Contract Variables
BTM_STORAGE_PREFIX = 'BTM'
BTM_CONTRACT  = 'CLOSED'
BTM_REGISTER_FEE = 0 * 100_000_000  # 10 to owners * 10^8 / for now/test free
BTM_Transfer_FEE = 0 * 100_000_000   # 5 to owners * 10^8 / for now/test free
BTM_CONTRACT_ADMIN = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
BTM_METHODS = ['QueryFarmContract', 'UnregisterFarmContract','RegisterFarmContract','TransferFarmContract']

#main program with contract operations
def Main(operation, args):
    nargs = len(args)
    if nargs == 0:
        print("No details entered")
        return 0

    # create a registry to address association for a small fee
    # can only be called by owner of address being registered
    ## Concatination point to the reffered registry

    elif operation == 'RegisterFarmContract':
        if nargs < 7:
            print("required arguments: [FarmContract] [owner]")
            return 0
        # elif get_participant_rating(args[1]) < 1:
        #      print("rating: [FarmContract] [owner]")
        FarmContract_name = args[0]
        OwnerNeoAddress = args[1]  
        Farmer_id  = args[2]  
        Buyer_id = args[3]  
        Project_id = args[4]  
        Contract_id = args[5]  
        Balance = args[6]  
        Status = args[7]  
        Other_data = args[8]

       # buyer_rating = get_participant_rating(Buyer_id)
        #farmer_rating = get_participant_rating(Farmer_id)
        # contract_rating = get_participant_rating(Contract_id)

        
      
        #first time registration smart contract rating
        # if farmer_rating =='':
        #    rate_participant(Farmer_id,5)
        # if buyer_rating =='':
        #    rate_participant(Buyer_id,5)
        # if contract_rating =='':
        #    rate_participant(Contract_id,5)

        # if farmer_rating < 2:
        #    print("Farmer has a poor rating") 
        # if buyer_rating < 2:
        #    print("Buyer has a poor rating")
          

        # print("Buyer Rating")
        # print(buyer_rating)
        # print("Farmer Rating")
        # print(farmer_rating)

       
        print("Register Farm Contract ")
        print("Entered Arguments: [FarmContract_name][OwnerNeoAddress][Farmer_id][Buyer_id][Project_id][Contract_id][Balance][Status][Other_data]")
        return RegisterFarmContract(FarmContract_name,OwnerNeoAddress,Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status,Other_data)


    ## Registrations that access different features of the agriculture smartcontracts   
    ## Retreive the address/name associated with a given name
    ## Anyone can call 
    ## Concatination point to the reffered registry

    elif operation == 'QueryFarmContract':
        FarmContract_name = args[0]
        OwnerNeoAddress = args[1]
        print("Query Farm Contract")
        print("Entered Arguments: [FarmContract_name] [OwnerNeoAddress]")
        return QueryFarmContract(FarmContract_name,OwnerNeoAddress)

    # remove a link between a given registry and it's address
    # can only be called by registry owner
    ## Concatination point to the reffered registry

    elif operation == 'UnregisterFarmContract':
        FarmContract_name = args[0]
        OwnerNeoAddress = args[1]
        print("Unregister Farm Contract ")
        print("Entered Arguments: [FarmContract_name] [OwnerNeoAddress]")
        return UnregisterFarmContract(FarmContract_name,OwnerNeoAddress)


## ~~~~~~~~~~~~~~~~~~~~~Digital Coupon and contract progress updates~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## This will be used to update contract balance and contract status
## A service from an oracle will be posting updates to 

    elif operation == 'UpdateFarmContract':
        if nargs < 7:
            print("required arguments: [FarmContract] [owner]")
            return 0
        FarmContract_name = args[0]
        OwnerNeoAddress = args[1]  
        Farmer_id  = args[2]  
        Buyer_id = args[3]  
        Project_id = args[4]  
        Contract_id = args[5]  
        Balance = args[6]  
        Status = args[7]  
        Other_data = args[8]

        print("Update Farm Contract Status")
        print("Entered Arguments: [FarmContract_name][OwnerNeoAddress][Farmer_id][Buyer_id][Project_id][Contract_id][Balance][Status][Other_data]")

        storage_key = concat(FarmContract_name, OwnerNeoAddress)
        context = GetContext()

        if not CheckWitness(OwnerNeoAddress):
               Notify("Owner argument is not the same as the person who registered")
               return False

        raw_data = [Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status,Other_data]
        farm_contract_info_serialised = serialize_array(raw_data)

        putRegistry(context, storage_key,farm_contract_info_serialised)
        return True
## ~~~~~~~~~~~~~~~~~~~~~Transfer ownership of farm contract~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # create Transfer of ownership of registry to new address association for a small fee
    # can only be called by owner of address being registered
    ## Concatination point to the reffered registry

    elif operation == 'TransferFarmContract':
        if nargs < 6:
            print("required arguments: [FarmContract] [owner]")
            return 0
        FarmContract_name = args[0]
        OwnerNeoAddress = args[1]  
        Farmer_id  = args[2]  
        Buyer_id = args[3]  
        Project_id = args[4]  
        Contract_id = args[5]  
        Balance = args[6]  
        Status = args[7]
        Other_data = args[8]  

        print("Update Farm Contract Status")
        print("Entered Arguments: [FarmContract_name][OwnerNeoAddress][Farmer_id][Buyer_id][Project_id][Contract_id][Balance][Status][Other_data]")

        storage_key = concat(FarmContract_name, OwnerNeoAddress)
        context = GetContext()

        if not CheckWitness(OwnerNeoAddress):
               Notify("Owner argument is not the same as the person who registered")
               return False

        raw_data = [Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status,Other_data]
        farm_contract_info_serialised = serialize_array(raw_data)
        UnregisterFarmContract(FarmContract_name,OwnerNeoAddress)
        putRegistry(context, storage_key,farm_contract_info_serialised)
        return True

## ~~~~~~~~~~~~~~~~~~~~~Contract Participants Rating System~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## A smart contract for rating buyers and farmers and creating a record based on this for future reference
## Add participant to rating contract
## calculate partcicipant rating
## update participant rating
## get participant rating 
## if rating from 1 ,2 3,4,5 , if rating is ==1 user cannot participant in contract anymore


    elif operation == 'RateFarmContractParticipant':
        OwnerNeoAddress= args[0]
        Rating = args[1]
        print("RateFarmContractParticipant")
        print("Entered Arguments:  [OwnerNeoAddress][Rating]")
        return rate_participant(OwnerNeoAddress,Rating)


    elif operation == 'GetParticipantRating':
        OwnerNeoAddress= args[0]
        print("RateFarmContractParticipant")
        print("Entered Arguments:  [OwnerNeoAddress]")
        return get_participant_rating(OwnerNeoAddress)


## core registry functions
def RegisterFarmContract(FarmContract_name,OwnerNeoAddress,Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status,Other_data):
    msg = concat("RegisterFarmContract: ", FarmContract_name)
    msg2 = concat(msg, OwnerNeoAddress)
    Notify(msg2)

    storage_key = concat(FarmContract_name, OwnerNeoAddress)

    if not CheckWitness(OwnerNeoAddress):
        Notify("Owner argument is not the same as the person who registered")
        return False

    context = GetContext()
    exists = getRegistry(context, storage_key)
    if exists:
        Notify("Contract is already registered")
        return False

    raw_data = [Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status,Other_data]
    farm_contract_info_serialised = serialize_array(raw_data)

    putRegistry(context, storage_key,farm_contract_info_serialised)
    return True

def QueryFarmContract(FarmContract_name,OwnerNeoAddress):
    msg = concat("QueryFarmContract: ", FarmContract_name)
    msg2 = concat(msg, OwnerNeoAddress)
    Notify(msg2)

    storage_key = concat(FarmContract_name, OwnerNeoAddress)

    context = GetContext()
    Owner = getRegistry(context, storage_key)
    if not Owner:
        Notify("This Farm Contract is not yet registered")
        return False
    farm_contract_info = deserialize_bytearray(Owner)
    Notify(farm_contract_info)
    return farm_contract_info

def UnregisterFarmContract(FarmContract_name,OwnerNeoAddress):
    msg = concat("UnregisterFarmContract: ", FarmContract_name)
    msg2 = concat(msg, OwnerNeoAddress)
    Notify(msg2)

    storage_key = concat(FarmContract_name, OwnerNeoAddress)

    context = GetContext()
    owner = getRegistry(context, storage_key)
    if not owner:
        Notify("FarmContract is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner of the FarmContract, the FarmContract cannot be deleted")
        return False

    removeRegistry(context, storage_key)
    return True

#rating methods


def rate_participant(OwnerNeoAddress,Rating):
    #Type = "StarRating" 
    ctx = GetContext()  

  
    if Rating == 1:
       print("one star")
       OwnerNeoAddressStar1 = concat(OwnerNeoAddress,"Star1")
       current_rating_count = getRegistry(ctx, OwnerNeoAddressStar1)
       new_rating_count = current_rating_count + 1
       putRegistry(ctx, OwnerNeoAddressStar1, new_rating_count)
    elif Rating == 2:
       print("two star")
       OwnerNeoAddressStar2 = concat(OwnerNeoAddress,"Star2")
       current_rating_count = getRegistry(ctx, OwnerNeoAddressStar2)
       new_rating_count = current_rating_count + 1
       putRegistry(ctx, OwnerNeoAddressStar2, new_rating_count)
    elif Rating == 3:
       print("three star")
       OwnerNeoAddressStar3 = concat(OwnerNeoAddress,"Star3")
       current_rating_count = getRegistry(ctx, OwnerNeoAddressStar3)
       new_rating_count = current_rating_count + 1
       putRegistry(ctx, OwnerNeoAddressStar3, new_rating_count)
    elif Rating == 4:
       print("four star")
       OwnerNeoAddressStar4 = concat(OwnerNeoAddress,"Star4")
       current_rating_count = getRegistry(ctx, new_rating_count)
       new_rating_count = current_rating_count + 1
       putRegistry(ctx, OwnerNeoAddressStar4, Rating)
    elif Rating == 5:
       print("five star")
       OwnerNeoAddressStar5 = concat(OwnerNeoAddress,"Star5")
       current_rating_count = getRegistry(ctx, new_rating_count)
       new_rating_count = current_rating_count + 1
       putRegistry(ctx, OwnerNeoAddressStar5, new_rating_count)

    return calculate_new_final_participant_rating(ctx,OwnerNeoAddress)

def calculate_new_final_participant_rating(ctx,OwnerNeoAddress):
      # update final rating  final_participant_rating = 
      #  example (5*252 + 4*124 + 3*40 + 2*29 + 1*33) / (252+124+40+29+33) = 4.11 and change
    OwnerNeoAddressStar1  = concat(OwnerNeoAddress,"Star1")
    OwnerNeoAddressStar2  = concat(OwnerNeoAddress,"Star2")
    OwnerNeoAddressStar3  = concat(OwnerNeoAddress,"Star3")
    OwnerNeoAddressStar4  = concat(OwnerNeoAddress,"Star4")
    OwnerNeoAddressStar5  = concat(OwnerNeoAddress,"Star5")

    current_rating_count1 = getRegistry(ctx, OwnerNeoAddressStar1)
    current_rating_count2 = getRegistry(ctx, OwnerNeoAddressStar2)
    current_rating_count3 = getRegistry(ctx, OwnerNeoAddressStar3)
    current_rating_count4 = getRegistry(ctx, OwnerNeoAddressStar4)
    current_rating_count5 = getRegistry(ctx, OwnerNeoAddressStar5)

    weighed = 5*current_rating_count5 + 4*current_rating_count4 + 3*current_rating_count3+ 2*current_rating_count2+ 1*current_rating_count1
    total  = current_rating_count1+current_rating_count2+current_rating_count3+current_rating_count4+current_rating_count5
    print("calculate new rating")
    calculate_new_final_participant_rating = (weighed/total)
    print("update new")
     # update final rating
    OwnerNeoAddressStarFinal = concat(OwnerNeoAddress,"StarFinal")
    putRegistry(ctx, OwnerNeoAddressStarFinal, calculate_new_final_participant_rating)

    return calculate_new_final_participant_rating


def get_participant_rating(OwnerNeoAddress):
    OwnerNeoAddressStarFinal = concat(OwnerNeoAddress,"StarFinal")
    ctx = GetContext()
    rating_key = getRegistry(ctx, OwnerNeoAddressStarFinal)
    print(rating_key)

    return rating_key 

# Contract Storage Functions

def putRegistry(ctx, key, value):
    return Put(ctx, prefixStorageKey(key), value)

def getRegistry(ctx, key):
    return Get(ctx,  prefixStorageKey(key))


def removeRegistry(ctx, key):
    return Delete(ctx, prefixStorageKey(key))


def prefixStorageKey(key):
    return concat(BTM_STORAGE_PREFIX, key)


