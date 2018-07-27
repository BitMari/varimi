# participant rating contract
# first version will not have fees for rating , fees will be added for users to be able to rating another user
# import  neo boa services

from boa.builtins import concat



#methods
## Add participant to rating contract
## calculate partcicipant rating
## update participant rating
## get participant rating 
## Weighed average
##  (5*252 + 4*124 + 3*40 + 2*29 + 1*33) / (252+124+40+29+33) = 4.11 and change
BTM_STORAGE_RATING_PREFIX = 'BTMR'

def rate_participant(OwnerNeoAddress,Rating):
    #Type = "StarRating" 
    ctx = GetContext()  
  
    if Rating == 1:
       print("one star")
       OwnerNeoAddressStar1 = concat(OwnerNeoAddress,"Star1")
       current_rating_count = getRegistry(ctx, OwnerNeoAddressStar1)
       new_rating_count = current_rating_count + 1
       putRegistry(ctx, OwnerNeoAddressStar1, new_rating_count)
    elif Rating == 2:
       print("two star")
       OwnerNeoAddressStar2 = concat(OwnerNeoAddress,"Star2")
       current_rating_count = getRegistry(ctx, OwnerNeoAddressStar2)
       new_rating_count = current_rating_count + 1
       putRegistry(ctx, OwnerNeoAddressStar2, new_rating_count)
    elif Rating == 3:
       print("three star")
       OwnerNeoAddressStar3 = concat(OwnerNeoAddress,"Star3")
       current_rating_count = getRegistry(ctx, OwnerNeoAddressStar3)
       new_rating_count = current_rating_count + 1
       putRegistry(ctx, OwnerNeoAddressStar3, new_rating_count)
    elif Rating == 4:
       print("four star")
       OwnerNeoAddressStar4 = concat(OwnerNeoAddress,"Star4")
       current_rating_count = getRegistry(ctx, new_rating_count)
       new_rating_count = current_rating_count + 1
       putRegistry(ctx, OwnerNeoAddressStar4, Rating)
    elif Rating == 5:
       print("five star")
       OwnerNeoAddressStar5 = concat(OwnerNeoAddress,"Star5")
       current_rating_count = getRegistry(ctx, new_rating_count)
       new_rating_count = current_rating_count + 1
       putRegistry(ctx, OwnerNeoAddressStar5, new_rating_count)
  
   # update final rating  final_participant_rating = 
     #  example (5*252 + 4*124 + 3*40 + 2*29 + 1*33) / (252+124+40+29+33) = 4.11 and change
       current_rating_count1 = getRegistry(ctx, OwnerNeoAddressStar1)
       current_rating_count2 = getRegistry(ctx, OwnerNeoAddressStar2)
       current_rating_count3 = getRegistry(ctx, OwnerNeoAddressStar3)
       current_rating_count4 = getRegistry(ctx, OwnerNeoAddressStar4)
       current_rating_count5 = getRegistry(ctx, OwnerNeoAddressStar5)

       weighed = 5*current_rating_count5 + 4*current_rating_count4 + 3*current_rating_count3+ 2*current_rating_count2+ 1*current_rating_count1
       total  = current_rating_count1+current_rating_count2+current_rating_count3+current_rating_count4+current_rating_count5
       print("calculate new rating")
       calculate_new_final_participant_rating = (weighed/total)
       print("update new")
     # update final rating
       OwnerNeoAddressStarFinal = concat(OwnerNeoAddress,"Star3")
       putRegistry(ctx, OwnerNeoAddressStarFinal, calculate_new_final_participant_rating)

    return calculate_new_final_participant_rating

def get_participant_rating(OwnerNeoAddress):
    OwnerNeoAddressStarFinal = concat(OwnerNeoAddress,"StarFinal")
    ctx = GetContext()
    rating_key = getRegistry(ctx, OwnerNeoAddressStarFinal)

    return rating_key 


# Contract Storage Functions

def putRegistry(ctx, key, value):
    return Put(ctx, prefixStorageKey(key), value)

def getRegistry(ctx, key):
    return Get(ctx,  prefixStorageKey(key))


def removeRegistry(ctx, key):
    return Delete(ctx, prefixStorageKey(key))


def prefixStorageKey(key):
    return concat(BTM_STORAGE_RATING_PREFIX, key)



