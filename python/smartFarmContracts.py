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

## Farmer 
    if operation == 'QueryFarmer':
        Farmer_name = args[0]
        return QueryFarmer(Farmer_name)

    elif operation == 'DeleteFarmer':
        Farmer_name = args[0]
        return DeleteFarmer(Farmer_name)

    elif operation == 'RegisterFarmer':
        if nargs < 2:
            print("required arguments: [Farmer_name] [owner]")
            return 0
        Farmer_name = args[0]
        owner = args[1]
        return RegisterFarmer(Farmer_name, owner)
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
     ##Buyer      
    elif operation == 'QueryBuyer':
        Buyer_name = args[0]
        return QueryBuyer(Buyer_name)

    elif operation == 'DeleteBuyer':
        Buyer_name = args[0]
        return DeleteBuyer(Buyer_name)

    elif operation == 'RegisterBuyer':
        if nargs < 2:
            print("required arguments: [Buyer_name] [owner]")
            return 0
        Buyer_name = args[0]
        owner = args[1]
        return RegisterBuyer(Buyer_name, owner)
  ##Smart Farm Contract       
    elif operation == 'QueryFarmContract':
        FarmContract_name = args[0]
        return QueryFarmContract(FarmContract_name)

    elif operation == 'DeleteFarmContract':
        FarmContract_name = args[0]
        return DeleteFarmContract(FarmContract_name)

    elif operation == 'RegisterFarmContract':
        if nargs < 2:
            print("required arguments: [FarmContract_name] [owner]")
            return 0
        FarmContract_name = args[0]
        owner = args[1]
        return RegisterFarm(FarmContract_name, owner)

    elif operation == 'TransferFarmContract':
        if nargs < 2:
            print("required arguments: [FarmContract_name] [to_address]")
            return 0
        FarmContract_name = args[0]
        to_address = args[1]
        return TransferFarm(FarmContract_name, to_address)




## STAGE ONE : FARMER REGISTRATION
## STAGE TWO : FARM REGISTRATION
## STAGE THREE : PROJECT REGISTRATION
## STAGE FOUR : Buyer REGISTRATION
## STAGE FIVE : SMART FARM CONTRACT BUYING AND FUNDING 
## STAGE SIX : DIGITAL COUPON REDEEMING/TOKENS ON SUPPLIER POS
## STAGE SEVEN : ROI AND PROJECT CLOSING 

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

## STAGE THREE : FARM PROJECT REGISTRATION : PYTHON CODE COMPLETE 
## THIS CODE IS TO REGISTER FARM PROJECT GIVEN THE FARMER IS ALSO ON THE BLOCKCHAIN AND THEIR FARM IS ALSO REGISTERED 
## ON THE BLOCKCHAIN WITH ABILITY TO ADD/DELETE/QUERY/TRANSFER OF PROJECT OWNERSHIP
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

## STAGE FOUR : Buyer REGISTRATION : PYTHON CODE COMPLETE 
## THIS CODE IS TO REGISTER A DIRECT Buyer ON THE BLOCKCHAIN WITH ABILITY TO ADD/DELETE/QUERY 
def QueryBuyer(Buyer_name):
    msg = concat("QueryBuyer: ", Buyer_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, Buyer_name)
    if not owner:
        Notify("This Buyer is not yet registered")
        return False

    Notify(owner)
    return owner


def RegisterBuyer(Buyer_name, owner):
    msg = concat("RegisterBuyer: ", Buyer_name)
    Notify(msg)

    if not CheckWitness(owner):
        Notify("Owner argument is not the same as the person who registered")
        return False

    context = GetContext()
    exists = Get(context, Buyer_name)
    if exists:
        Notify("Buyer is already registered")
        return False

    Put(context, Buyer_name, owner)
    return True



def DeleteBuyer(Buyer_name):
    msg = concat("DeleteBuyer: ", Buyer_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, Buyer_name)
    if not owner:
        Notify("Buyer is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner of the name, the Buyer cannot be deleted")
        return False

    Delete(context, Buyer_name)
    return True

## STAGE FIVE : THE BITMARI SMART FARM CONTRACT : PYTHON CODE COMPLETE 
## THIS CODE IS TO CREATE A RECORD BETWEEN The Buyer AND With Terms of the contract 
## ON THE BLOCKCHAIN WITH ABILITY TO ADD/DELETE/QUERY/TRANSFER/ (STAGE SEVEN) OF  CONTRACT OWNERSHIP
## THE ORACLE WILL BE THE SUPPLIER POS
def QueryFarmContract(FarmContract_name):
    msg = concat("QueryFarmContract: ", FarmContract_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, FarmContract_name)
    if not owner:
        Notify("This farm Contract is not yet registered")
        return False

    Notify(owner)
    return owner


def RegisterFarmContract(FarmContract_name, owner):
    msg = concat("RegisterFarmContract: ", FarmContract_name)
    Notify(msg)

    if not CheckWitness(owner):
        Notify("Owner argument is not the same as the person who registered")
        return False

    context = GetContext()
    exists = Get(context, FarmContract_name)
    if exists:
        Notify("Farm Contract is already registered")
        return False

    Put(context, FarmContract_name, owner)
    return True


def TransferFarmContract(FarmContract_name, to_address):
    msg = concat("TransferFarmContract: ", FarmContract_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, FarmContract_name)
    if not owner:
        Notify("Farm Contract is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner, farm Contract ownership cannot transfer")
        return False

    if not len(to_address) != 34:
        Notify("Invalid new owner neo address. Must be exactly 34 characters")
        return False

    Put(context, FarmContract_name, to_address)
    return True


def DeleteFarmContract(FarmContract_name):
    msg = concat("DeleteFarmContract: ", FarmContract_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, FarmContract_name)
    if not owner:
        Notify("Farm Contract is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("This person is not the owner of the farm Contract, the farm Contract cannot be deleted")
        return False

    Delete(context, FarmContract_name)
    return True

#### STAGE SIX : DIGITAL COUPON USE 
#### CONTRACT NEEDS TO HAVE ADRESSES AND DIGITAL COUPONS USE
### CHECK BALANCE/TRANSFER BALANCE / SALE FROM POS / TILL BALANCE IS ZERO/ USE GAS / EACH FARMER HAS A BALANCE SHARED WITH BUYER 
