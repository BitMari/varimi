## STAGE FOUR : Contract REGISTRATION
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
        print("No Farmer name supplied")
        return 0
  ##Contract      
    elif operation == 'QueryContract':
        Contract_name = args[0]
        return QueryContract(Contract_name)

    elif operation == 'DeleteContract':
        Contract_name = args[0]
        return DeleteContract(Contract_name)

    elif operation == 'RegisterContract':
        if nargs < 2:
            print("required arguments: [Contract_name] [owner]")
            return 0
        Contract_name = args[0]
        owner = args[1]
        return RegisterContract(Contract_name, owner)
        
## STAGE FOUR : Contract REGISTRATION : PYTHON CODE COMPLETE 
## THIS CODE IS TO REGISTER A DIRECT Contract ON THE BLOCKCHAIN WITH ABILITY TO ADD/DELETE/QUERY 
def QueryContract(Contract_name):
    msg = concat("QueryContract: ", Contract_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, Contract_name)
    if not owner:
        Notify("This Contract is not yet registered")
        return False

    Notify(owner)
    return owner

def RegisterContract(Contract_name, owner):
    msg = concat("RegisterContract: ", Contract_name)
    Notify(msg)

    if not CheckWitness(owner):
        Notify("Owner argument is not the same as the person who registered")
        return False

    context = GetContext()
    exists = Get(context, Contract_name)
    if exists:
        Notify("Contract is already registered")
        return False

    Put(context, Contract_name, owner)
    return True

def DeleteContract(Contract_name):
    msg = concat("DeleteContract: ", Contract_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, Contract_name)
    if not owner:
        Notify("Contract is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner of the contract, the Contract cannot be deleted")
        return False

    Delete(context, Contract_name)
    return True
