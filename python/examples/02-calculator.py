
# BUILD TEST
# build smartContracts/02-calculator.py test 070202 02 False False plus 1 1
#
# IMPORT
# import contract smartContracts/02-calculator.avm 070202 02 False False
#
# INVOKE
# testinvoke <your_contract_hash> plus 1 1

def Main(operation, foo, bar):

    if operation == None or foo == None or bar == None:
        print('Operation, foo, and bar all required~!')
        return False

    if operation == 'plus':
        print('plus')
        return foo + bar

    if operation == 'minus':
        print('minus')
        return foo - bar

    if operation == 'multiply':
        print('multiply')
        return foo * bar

    if operation == 'divide':
        print('divide')
        return foo / bar

    print('invalid operation')
    print(operation)
return False