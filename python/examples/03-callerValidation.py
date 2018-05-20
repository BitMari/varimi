
# A simple function to demonstrate the usage of CheckWitness
# This contract will validate the provided input key/hash matches that of callerHash
#
# BUILD TEST
# True return
# build smartContracts/03-callerValidation.py test 06 01 False False <your_wallet_address>
# False return
# build smartContracts/03-callerValidation.py test 06 01 False False 11111
#
# IMPORT
# import contract smartContracts/03-callerValidation.avm 06 01 False False
#
# INVOKE
# testinvoke <your_contract_hash> plus 1 1

from boa.blockchain.vm.Neo.Runtime import CheckWitness

def Main(callerHash):

    isMatch = CheckWitness(callerHash)

    if isMatch:
        print("Caller hash/key matches provided hash/key!")
        return True

    print("IMPOSTER!!!")
return False