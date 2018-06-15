#Utility to add or remove items from arrays
def removeItem(array, item):
    newList = []
    for currentItem in array:
        if currentItem != item:
            newList.append(currentItem)
    return newList

def addItem(array, item):
    newList = []
    for currentItem in array:
        newList.append(currentItem)
    newList.append(item)
    return newList