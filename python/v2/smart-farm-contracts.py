# The Main BitMari Smart Farm Contract 
# All other features of the contract will be accesed from this file
# These include land registration , digital coupon and farm contract registration

# import  neo services
from boa.interop.Neo.Runtime import Log, Notify, GetTrigger, CheckWitness
from boa.interop.Neo.Action import RegisterAction

from boa.interop.Neo.TransactionType import InvocationTransaction
from boa.interop.Neo.Transaction import *

from boa.interop.System.ExecutionEngine import InvocationTransaction
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Output import GetScriptHash, GetValue, GetAssetId
from boa.interop.Neo.Storage import Get, Put,Delete, GetContext

from boa.builtins import concat

# import btm points 
from btm.txio import get_asset_attachments
from btm.token import *
from btm.crowdsale import *
from btm.nep5 import *
from btm.arrayUtil import *
from btm.serialization import *

# import other agriculture contracts

# Contract Variables
NS_STORAGE_PREFIX = 'BSFC'

## conversion meanings: what details enter into contract memory actualy mean 
## 1.RT : Registry Types : these include f
## - farmRegistry :LR (Land Registry)
## - farmerRegistry: FR
## - farmProjectRegistry: FPR
## - buyerRegistry: BR
## - farmContractRegistry : FCR


#main program with contract operations
def Main(operation, args):
    nargs = len(args)
    if nargs == 0:
        print("No details entered")
        return 0
  ##Registrations that access different features of the agriculture smartcontracts   
  # retreive the address/name associated with a given name
  # anyone can call 
    elif operation == 'QueryRegistry':
        Registry_name = args[0]
        return QueryRegistry(Registry_name)

    elif operation == 'DeleteRegistry':
        Registry_name = args[0]
        return DeleteRegistry(Registry_name)

    elif operation == 'RegisterRegistry':
        if nargs < 2:
            print("required arguments: [Registry_name] [owner]")
            return 0
        Registry_name = args[0]
        owner = args[1]
        return RegisterRegistry(Registry_name, owner)

     elif operation == 'TransferRegistry':
        if nargs < 2:
            print("required arguments: [Registry_name] [to_address]")
            return 0
        Registry_name = args[0]
        to_address = args[1]
        return TransferRegistry(Registry_name, to_address) 

## functions
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

    deleteRegistry(context, Registry_name)
    return True


 # Contract Storage Functions



def putRegistry(ctx, key, value):
    return Put(ctx, prefixStorageKey(key), value)


def getRegistry(ctx, key):
    return Get(ctx,  prefixStorageKey(key))


def deleteRegistry(ctx, key):
    return Delete(ctx, prefixStorageKey(key))

## Add prefix to records

def prefixStorageKey(key):
return concat(NS_STORAGE_PREFIX, key)


 # nameConcat = concat(name, newOwnerAddress)
 #    nameConcat = concat('OFFER', nameConcat)
 #    currentOffer = getName(ctx, nameConcat)
