# BUILD TEST
# build smartContracts/04-concat.py test 0710 07 False False subshine ['hello','world','things','otherthings']
#
# IMPORT
# import contract smartContracts/04-concat.avm 0710 07 False False
#
# INVOKE
# testinvoke <your_contract_hash> subshine ['hello','world','things','otherthings']

from boa.code.builtins import concat

def Main(initialString, args):

    result = initialString
    for word in args:
        if result == None:
            result = word
        else:
            result = concat(result," ")
            result = concat(result,word)
        print(result)

return result