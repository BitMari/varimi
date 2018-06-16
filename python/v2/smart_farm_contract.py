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
##  build /smart-contracts/smart-farm-contracts.py    0x12f4f99e6f61ced8d41683c84a33b1bb2c9b49c6
##  import contract /smart-contracts/smart-farm-contracts.avm 0710 05 True False
## testinvoke 12f4f99e6f61ced8d41683c84a33b1bb2c9b49c6 RegisterRegistry ["Tongayi","AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y", "{'name':'Tongayi', 'surname': 'Choto','age':'30', 'gender':'male'}"]
## testinvoke 12f4f99e6f61ced8d41683c84a33b1bb2c9b49c6 QueryRegistry ["Tongayi"]
## testinvoke 3889c247702188d30fb9f864b7f01f4f95635010 RemoveRegistry ["BSFCuserneoaddress.type.name.surname","AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y"]
##
## testinvoke 3889c247702188d30fb9f864b7f01f4f95635010 TransferRegistry ["BSFCuserneoaddress.type.name.surname","AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y"]
## 
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
        print("Register Farm Contract ")
        print("Entered Arguments: [FarmContract_name][OwnerNeoAddress][Farmer_id][Buyer_id][Project_id][Contract_id][Balance][Status]")
        return RegisterFarmContract(FarmContract_name,OwnerNeoAddress,Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status)


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

    # create Transfer of ownership of registry to new address association for a small fee
    # can only be called by owner of address being registered
    ## Concatination point to the reffered registry

    elif operation == 'TransferFarmContract':
        if nargs < 2:
            print("required arguments: [FarmContract_name] [OwnerNeoAddress] [to_address]")
            return 0
        FarmContract_name = args[0]
        OwnerNeoAddress = args[1]
        to_address = args[2]
        print("Transfer Farm Contract ")
        print("Entered Arguments: [FarmContract_name][OwnerNeoAddress][to_address]")
        return TransferFarmContract(FarmContract_name,OwnerNeoAddress, to_address) 

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

    elif operation == 'UpdateFarmContract':
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

        print("Update Farm Contract Status")
        print("Entered Arguments: [FarmContract_name][OwnerNeoAddress][Farmer_id][Buyer_id][Project_id][Contract_id][Balance][Status]")

        storage_key = concat(FarmContract_name, OwnerNeoAddress)
        context = GetContext()

        if not CheckWitness(OwnerNeoAddress):
               Notify("Owner argument is not the same as the person who registered")
               return False

        raw_data = [Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status]
        farm_contract_info_serialised = serialize_array(raw_data)

        putRegistry(context, storage_key,farm_contract_info_serialised)
        return True




## core registry functions
def RegisterFarmContract(FarmContract_name,OwnerNeoAddress,Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status):
    msg = concat("RegisterFarmContract: ", FarmContract_name)
    msg2 = concat(msg, OwnerNeoAddress)
    Notify(msg2)

    storage_key = concat(FarmContract_name, OwnerNeoAddress)

    if not CheckWitness(OwnerNeoAddress):
        Notify("Owner argument is not the same as the person who registered")
        return False

    context = GetContext()
    exists = Get(context, storage_key)
    if exists:
        Notify("Contract is already registered")
        return False

    raw_data = [Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status]
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

def TransferFarmContract(FarmContract_name,OwnerNeoAddress, to_address):
    msg = concat("TransferFarmContract: ", FarmContract_name)
    msg2 = concat(msg, OwnerNeoAddress)
    Notify(msg2)

    storage_key = concat(FarmContract_name, OwnerNeoAddress)

    context = GetContext()
    Owner = Get(context, storage_key)
    if not Owner:
        Notify("This farm contract is not yet registered")
        return False

    if not CheckWitness(Owner):
        Notify("This person is not the Owner, Farm Contract ownership cannot be Transfered")
        return False

    if not len(to_address) != 34:
        Notify("Invalid new owner neo address. Must be exactly 34 characters")
        return False

    putRegistry(context, storage_key, to_address)
    return True


def UnregisterFarmContract(FarmContract_name,OwnerNeoAddress):
    msg = concat("UnregisterFarmContract: ", FarmContract_name)
    msg2 = concat(msg, OwnerNeoAddress)
    Notify(msg2)

    storage_key = concat(FarmContract_name, OwnerNeoAddress)

    context = GetContext()
    owner = Get(context, storage_key)
    if not owner:
        Notify("FarmContract is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner of the FarmContract, the FarmContract cannot be deleted")
        return False

    removeRegistry(context, storage_key)
    return True


# Contract Storage Functions

def putRegistry(ctx, key, value):
    return Put(ctx, prefixStorageKey(key), value)

def getRegistry(ctx, key):
    return Get(ctx,  prefixStorageKey(key))


def removeRegistry(ctx, key):
    return Delete(ctx, prefixStorageKey(key))


def prefixStorageKey(key):
    return concat(BTM_STORAGE_PREFIX, key)


