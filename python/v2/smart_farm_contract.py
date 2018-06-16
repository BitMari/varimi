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
# from btm.serialization import *

# import other agriculture contracts

# Contract Variables
BTM_STORAGE_PREFIX = 'BTMSMARTCONTRACT'
BTM_CONTRACT  = 'CLOSED'
BTM_REGISTER_FEE = 0 * 100_000_000  # 10 to owners * 10^8 / for now/test free
BTM_TRANSFER_FEE = 0 * 100_000_000   # 5 to owners * 10^8 / for now/test free
BTM_CONTRACT_ADMIN = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
BTM_METHODS = ['QueryFarmContract','QueryFarmContractAddress', 'UnregisterFarmContract','RegisterFarmContract','TransferFarmContract']

#main program with contract operations
def Main(operation, args):
    nargs = len(args)
    if nargs == 0:
        print("No details entered")
        return 0

    ## Registrations that access different features of the agriculture smartcontracts   
    ## Retreive the address/name associated with a given name
    ## Anyone can call 
    ## Concatination point to the reffered registry

    elif operation == 'QueryFarmContract':
        FarmContract_name = args[0]
        print("Query Farm Contract")
        print("Entered Arguments: [FarmContract_name]")
        return QueryFarmContract(FarmContract_name)

    # Retreive a list of details associated with this address
    # Anyone can call
    # Output: array as bytearray
    ## Concatination point to the reffered registry

    elif operation == 'QueryFarmContractAddress':
        Owner_address = args[0]
        print("Query Farm Contract Address")
        print("Entered Arguments: [Owner_address]")
        return QueryFarmContractAddress(Owner_address)

    # remove a link between a given registry and it's address
    # can only be called by registry owner
    ## Concatination point to the reffered registry

    elif operation == 'UnregisterFarmContract':
        FarmContract_name = args[0]
        print("Unregister Farm Contract ")
        print("Entered Arguments: [FarmContract_name]")
        return UnregisterFarmContract(FarmContract_name)

    # create a registry to address association for a small fee
    # can only be called by owner of address being registered
    ## Concatination point to the reffered registry

    elif operation == 'RegisterFarmContract':
        if nargs < 6:
            print("required arguments: [FarmContract] [owner]")
            return 0
        FarmContract_name = args[0]
        Owner = args[1]  
		Farmer_id  = args[2]  
		Buyer_id = args[3]  
		Project_id = args[4]  
		Contract_id = args[5]  
		Balance = args[6]  
		Status = args[7]  
        print("Register Farm Contract ")
        print("Entered Arguments: [FarmContract_name][Owner][Farmer_id][Buyer_id][Project_id][Contract_id][Balance][Status]")
        return RegisterFarmContract(FarmContract_name,Owner,Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status)

    # create transfer of ownership of registry to new address association for a small fee
    # can only be called by owner of address being registered
    ## Concatination point to the reffered registry

    elif operation == 'TransferFarmContract':
        if nargs < 2:
            print("required arguments: [FarmContract_name] [to_address]")
            return 0
        FarmContract_name = args[0]
        to_address = args[1]
        print("Transfer Farm Contract ")
        print("Entered Arguments: [FarmContract_name] [to_address]")
        return TransferFarmContract(FarmContract_name, to_address) 



## core registry functions
def QueryFarmContract(FarmContract_name):
    msg = concat("QueryFarmContract: ", FarmContract_name)
    Notify(msg)

    context = GetContext()
    Owner = getRegistry(context, FarmContract_name)
    if not owner:
        Notify("This Farm Contract is not yet registered")
        return False

    Notify(Owner)
    return Owner


def RegisterFarmContract(FarmContract_name,Owner,Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status):
    msg = concat("RegisterRegistry: ", Registry_name)
    Notify(msg)

    if not CheckWitness(owner):
        Notify("Owner argument is not the same as the person who registered")
        return False

    context = GetContext()
    exists = Get(context, Registry_name)
    if exists:
        Notify("Registry is already registered")
        return False

    putRegistry(context, FarmContract_name,Owner,Farmer_id,Buyer_id,Project_id,Contract_id,Balance,Status)
    return True


def TransferFarmContract(FarmContract_name, to_address):
    msg = concat("TransferFarmContract: ", FarmContract_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, FarmContract_name)
    if not owner:
        Notify("Registry is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner, Registry ownership cannot be transfered")
        return False

    if not len(to_address) != 34:
        Notify("Invalid new owner neo address. Must be exactly 34 characters")
        return False

    putRegistry(context, FarmContract_name, to_address)
    return True


def UnregisterFarmContract(FarmContract_name):
    msg = concat("RemoveFarmContract: ", FarmContract_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, FarmContract_name)
    if not owner:
        Notify("FarmContract is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner of the FarmContract, the FarmContract cannot be deleted")
        return False

    removeRegistry(context, FarmContract_name)
    return True

#Generate storage key  storageKey = CreateStorageKey(A,B)

def CreateStorageKey(s1, s2):
    """Concatenate arguments for use as storage key.
    
    Args:
        s1 (str):
            first string to be used in concatenation.
        s2 (str):
            second string to be used in concatenation.
    Return:
        (str): args concatenated together with a '.' between each value.
    """

    withPeriod = concat(s1, '.')
    return concat(withPeriod, s2)

 # Contract Storage Functions



def putRegistry(ctx, key, value):
    return Put(ctx, prefixStorageKey(key), value)


def getRegistry(ctx, key):
    return Get(ctx,  prefixStorageKey(key))


def removeRegistry(ctx, key):
    return Delete(ctx, prefixStorageKey(key))

## Add prefix to records

def prefixStorageKey(key):
    return concat(BTM_STORAGE_PREFIX, key)


