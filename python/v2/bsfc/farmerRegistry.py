## STAGE ONE : FARMER REGISTRATION
"""
Testing:
neo> build varimi/smartFarmContracts.py test 0710 05 True False query ["Name"]
neo> build varimi/smartFarmContracts.py test 0710 05 True False register ["Name","AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y"]
neo> build varimi/smartFarmContracts.py test 0710 05 True False delete ["Name"]
neo> build varimi/smartFarmContracts.py test 0710 05 True False transfer ["Name","AK2nJJpJr6o664CWJKi1QRXjqeic"]
Importing:
neo> import contract varimi/smartFarmContracts.avm 0710 05 True False
import contract varimi/smartFarmContracts.avm 0710 05 True False
neo> contract search ...
Using:
neo> testinvoke c4e31aa5d66d7c9e8a4afa3a92be7e8a3ca49f76 query ["name"]
ed72a3d1e35420a8208f3f32e8e2815370ed1ed3

Examples


testinvoke ed72a3d1e35420a8208f3f32e8e2815370ed1ed3 RegisterFarmer ["Name","AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y"]
testinvoke ed72a3d1e35420a8208f3f32e8e2815370ed1ed3 QueryFarmer ["Name"]

"""
from boa.interop.Neo.Runtime import Log, Notify, GetTrigger, CheckWitness
from boa.interop.Neo.Action import RegisterAction

from boa.interop.Neo.TransactionType import InvocationTransaction
from boa.interop.Neo.Transaction import *

from boa.interop.System.ExecutionEngine import InvocationTransaction
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Output import GetScriptHash, GetValue, GetAssetId
from boa.interop.Neo.Storage import Get, Put,Delete, GetContext

from boa.builtins import concat


def Main(operation, args):
    nargs = len(args)
    if nargs == 0:
        print("No Farmer name supplied")
        return 0
 ##Farm       
    elif operation == 'QueryFarmer':
        Farmer_name = args[0]
        return QueryFarmer(Farmer_name)

    elif operation == 'DeleteFarmer':
        Farmer_name = args[0]
        return DeleteFarmer(Farmer_name)

    elif operation == 'RegisterFarmer':
        if nargs < 2:
            print("required arguments: [Farm_namer] [owner]")
            return 0
        Farmer_name = args[0]
        owner = args[1]
        return RegisterFarmer(Farmer_name, owner)
    



## STAGE ONE : FARMER REGISTRATION : PYTHON CODE COMPLETE 
## THIS CODE IS TO REGISTER A FARMER ON THE BLOCKCHAIN WITH ABILITY TO ADD/DELETE/QUERY FOR TRACKING

def QueryFarmer(Farmer_name):
    msg = concat("QueryFarmer: ", Farmer_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, Farmer_name)
    if not owner:
        Notify("This farmer is not yet registered")
        return False

    Notify(owner)
    return owner

def RegisterFarmer(Farmer_name, owner):
    msg = concat("RegisterFarmer: ", Farmer_name)
    Notify(msg)

    if not CheckWitness(owner):
        Notify("Owner argument is not the same as the person who registered the farmer")
        return False

    context = GetContext()
    exists = Get(context, Farmer_name)
    if exists:
        Notify("Farmer is already registered")
        return False

    Put(context, Farmer_name, owner)
    return True


def DeleteFarmer(Farmer_name):
    msg = concat("DeleteFarmer: ", Farmer_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, Farmer_name)
    if not owner:
        Notify("Farmer is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner of the farmer registry, the farmer cannot be deleted")
        return False

    Delete(context, Farmer_name)
    return True