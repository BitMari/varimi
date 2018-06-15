
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
BTM_METHODS = ['nameServiceQuery','nameServiceRegister', 'nameServiceCancelForSale']

## All contract registrations will have registry types, for the initial version they will not be enforced directly in the contract
## RT : Registry Types : these are
## - assetRegistry :     AR  (e.g Land , car , etc which translates to ARL(asset registry land))
## - userRegistry:       UR  (e.g farmer,buyer etc which translates to URF(user registry farmer))
## - projectRegistry:    PR  (e.g tomatoes,maize etc  which translates to PRT(project registry tomatoes))
## - contractRegistry :  CR  (this is when a contract between participants is registerd, which translates to CRA(contract registry agriculture) )
## - settingsRegistry :  SR  (store contract settings this include oracles , fee data , other agreements , which translates to SRX(settings registry x, where x is the contract registry with the settings)
## - attribute = {'project_id', 'title','duration'} AN EXPERIMENT WITH ARRAYS

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

    elif operation == 'QueryRegistry':
        Registry_name = args[0]
        Registry_type = args[1]
        QueryRegistryConcat = concat(Registry_type, Registry_name) 
        return QueryRegistry(QueryRegistryConcat)

    # Retreive a list of details associated with this address
    # Anyone can call
    # Output: array as bytearray
    ## Concatination point to the reffered registry

    elif operation == 'QueryRegistryAddress':
        Registry_address = args[0]
        Registry_type = args[1]
        QueryRegistryAddressConcat = concat(Registry_type, Registry_address) 
        return QueryRegistry(QueryRegistryAddressConcat)

    # remove a link between a given registry and it's address
    # can only be called by registry owner
    ## Concatination point to the reffered registry

    elif operation == 'RemoveRegistry':
        Registry_name = args[0]
        Registry_type = args[1]
        RemoveRegistryConcat = concat(Registry_type, Registry_name) 
        return RemoveRegistry(Registry_name)

    # create a registry to address association for a small fee
    # can only be called by owner of address being registered
    ## Concatination point to the reffered registry

    elif operation == 'RegisterRegistry':
        if nargs < 2:
            print("required arguments: [Registry_name] [owner]")
            return 0
        Registry_name = args[0]
        owner = args[1]
        Registry_type = args[2]
        RegisterRegistryConcat = concat(Registry_type, Registry_name) 
        return RegisterRegistry(RegisterRegistryConcat, owner)

    # create transfer of ownership of registry to new address association for a small fee
    # can only be called by owner of address being registered
    ## Concatination point to the reffered registry

    elif operation == 'TransferRegistry':
        if nargs < 2:
            print("required arguments: [Registry_name] [to_address]")
            return 0
        Registry_name = args[0]
        to_address = args[1]
        Registry_type = args[2]
        RegisterRegistryConcat = concat(Registry_type, Registry_name) 
        return TransferRegistry(RegisterRegistryConcat, to_address) 

   

    #smart contract functionalities which include different registry distinctions
    #S ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   




## core registry functions
def QueryRegistry(Registry_name):
    msg = concat("QueryRegistry: ", Registry_name)
    Notify(msg)

    context = GetContext()
    owner = getRegistry(context, Registry_name)
    if not owner:
        Notify("This Registry is not yet registered")
        return False

    Notify(owner)
    return owner


def RegisterRegistry(Registry_name, owner):
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

    putRegistry(context, Registry_name, owner)
    return True


def TransferRegistry(Registry_name, to_address):
    msg = concat("TransferRegistry: ", Registry_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, Registry_name)
    if not owner:
        Notify("Registry is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner, Registry ownership cannot be transfered")
        return False

    if not len(to_address) != 34:
        Notify("Invalid new owner neo address. Must be exactly 34 characters")
        return False

    putRegistry(context, Registry_name, to_address)
    return True


def RemoveRegistry(Registry_name):
    msg = concat("RemoveRegistry: ", Registry_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, Registry_name)
    if not owner:
        Notify("Registry is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner of the Registry, th Registry cannot be deleted")
        return False

    removeRegistry(context, Registry_name)
    return True

 # Get transaction hash transactionHash = GetTransactionHash()
 def GetTransactionHash():
    """Fetches the hash of the current transaction.
    Return:
        (str): hash of current transaction.
    """

    transaction = GetScriptContainer()
    hash = GetTransactionHash(transaction)
    return hash

#Generate storage key  storageKey = CreateStorageKey(alpha, beta)

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
    return concat(NS_STORAGE_PREFIX, key)


 # nameConcat = concat(name, newOwnerAddress)
 #    nameConcat = concat('OFFER', nameConcat)
 #    currentOffer = getName(ctx, nameConcat)
