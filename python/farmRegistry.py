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

testinvoke ed72a3d1e35420a8208f3f32e8e2815370ed1ed3 QueryFarmer ["tongayi"]
testinvoke ed72a3d1e35420a8208f3f32e8e2815370ed1ed3 QueryBuyer ["tongayi"]
testinvoke ed72a3d1e35420a8208f3f32e8e2815370ed1ed3 QueryFarmProject ["tongayi"]
testinvoke ed72a3d1e35420a8208f3f32e8e2815370ed1ed3 QueryFarmContract ["tongayi"]

testinvoke ed72a3d1e35420a8208f3f32e8e2815370ed1ed3 RegisterFarmer ["Name","AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y"]
testinvoke ed72a3d1e35420a8208f3f32e8e2815370ed1ed3 QueryFarmer ["Name"]

"""
from boa.blockchain.vm.Neo.Runtime import Log, Notify, GetTrigger, CheckWitness
from boa.blockchain.vm.Neo.Action import RegisterAction

from boa.blockchain.vm.Neo.TransactionType import InvocationTransaction
from boa.blockchain.vm.Neo.Transaction import *

from boa.blockchain.vm.System.ExecutionEngine import InvocationTransaction
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
from boa.blockchain.vm.Neo.Output import GetScriptHash, GetValue, GetAssetId
from boa.blockchain.vm.Neo.Storage import Get, Put,Delete, GetContext

from boa.code.builtins import concat


def Main(operation, args):
    nargs = len(args)
    if nargs == 0:
        print("No Farm name supplied")
        return 0
 ##Farm       
    elif operation == 'QueryFarm':
        Farm_name = args[0]
        return QueryFarm(Farm_name)

    elif operation == 'DeleteFarm':
        Farm_name = args[0]
        return DeleteFarm(Farm_name)

    elif operation == 'RegisterFarm':
        if nargs < 2:
            print("required arguments: [Farm_name] [owner]")
            return 0
        Farm_name = args[0]
        owner = args[1]
        return RegisterFarm(Farm_name, owner)

    elif operation == 'TransferFarm':
        if nargs < 2:
            print("required arguments: [Farm_name] [to_address]")
            return 0
        Farm_name = args[0]
        to_address = args[1]
        return TransferFarm(Farm_name, to_address)
    



## STAGE TWO : FARM REGISTRATION


## STAGE TWO : FARM REGISTRATION : PYTHON CODE COMPLETE 
## THIS CODE IS TO REGISTER FARM OWNERSHIP ON THE BLOCKCHAIN WITH ABILITY TO ADD/DELETE/QUERY/TRANSFER OWNERSHIP
def QueryFarm(Farm_name):
    msg = concat("QueryFarm: ", Farm_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, Farm_name)
    if not owner:
        Notify("This farm is not yet registered")
        return False

    Notify(owner)
    return owner


def RegisterFarm(Farm_name, owner):
    msg = concat("RegisterFarm: ", Farm_name)
    Notify(msg)

    if not CheckWitness(owner):
        Notify("Owner argument is not the same as the person who registered")
        return False

    context = GetContext()
    exists = Get(context, Farm_name)
    if exists:
        Notify("Farm is already registered")
        return False

    Put(context, Farm_name, owner)
    return True


def TransferFarm(Farm_name, to_address):
    msg = concat("TransferFarm: ", Farm_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, Farm_name)
    if not owner:
        Notify("Farm is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner, farm ownership cannot transfer")
        return False

    if not len(to_address) != 34:
        Notify("Invalid new owner neo address. Must be exactly 34 characters")
        return False

    Put(context, Farm_name, to_address)
    return True


def DeleteFarm(Farm_name):
    msg = concat("DeleteFarm: ", Farm_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, Farm_name)
    if not owner:
        Notify("Farm is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner of the farm, the farm cannot be deleted")
        return False

    Delete(context, Farm_name)
    return True
