## STAGE THREE : PROJECT REGISTRATION

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

testinvoke ed72a3d1e35420a8208f3f32e8e2815370ed1ed3 RegisterFarmProject ["Name","AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y"]
testinvoke ed72a3d1e35420a8208f3f32e8e2815370ed1ed3 QueryFarmProject ["Name"]

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




## STAGE THREE : FARM PROJECT REGISTRATION : PYTHON CODE COMPLETE 
## THIS CODE IS TO REGISTER FARM PROJECT GIVEN THE FARMER IS ALSO ON THE BLOCKCHAIN AND THEIR FARM IS ALSO REGISTERED 
## ON THE BLOCKCHAIN WITH ABILITY TO ADD/DELETE/QUERY/TRANSFER OF PROJECT OWNERSHIP


def Main(operation, args):
    nargs = len(args)
    if nargs == 0:
        print("No Argument supplied")
        return 0
       ##Project       
    elif operation == 'QueryFarmProject':
        FarmProject_name = args[0]
        return QueryFarmProject(FarmProject_name)

    elif operation == 'DeleteFarmProject':
        FarmProject_name = args[0]
        return DeleteFarmProject(FarmProject_name)

    elif operation == 'RegisterFarmProject':
        if nargs < 2:
            print("required arguments: [FarmProject_name] [owner]")
            return 0
        FarmProject_name = args[0]
        owner = args[1]
        return RegisterFarmProject(FarmProject_name, owner)

    elif operation == 'TransferFarmProject':
        if nargs < 2:
            print("required arguments: [FarmProject_name] [to_address]")
            return 0
        FarmProject_name = args[0]
        to_address = args[1]
        return TransferFarmProject(FarmProject_name, to_address) 
        
           
def QueryFarmProject(FarmProject_name):
    msg = concat("QueryFarmProject: ", FarmProject_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, FarmProject_name)
    if not owner:
        Notify("This farm project is not yet registered")
        return False

    Notify(owner)
    return owner


def RegisterFarmProject(FarmProject_name, owner):
    msg = concat("RegisterFarmProject: ", FarmProject_name)
    Notify(msg)

    if not CheckWitness(owner):
        Notify("Owner argument is not the same as the person who registered")
        return False

    context = GetContext()
    exists = Get(context, FarmProject_name)
    if exists:
        Notify("Farm Project is already registered")
        return False

    Put(context, FarmProject_name, owner)
    return True


def TransferFarmProject(FarmProject_name, to_address):
    msg = concat("TransferFarmProject: ", FarmProject_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, FarmProject_name)
    if not owner:
        Notify("Farm Project is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner, farm project ownership cannot transfer")
        return False

    if not len(to_address) != 34:
        Notify("Invalid new owner neo address. Must be exactly 34 characters")
        return False

    Put(context, FarmProject_name, to_address)
    return True


def DeleteFarmProject(FarmProject_name):
    msg = concat("DeleteFarmProject: ", FarmProject_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, FarmProject_name)
    if not owner:
        Notify("Farm Project is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner of the farm project, the farm project cannot be deleted")
        return False

    Delete(context, FarmProject_name)
    return True