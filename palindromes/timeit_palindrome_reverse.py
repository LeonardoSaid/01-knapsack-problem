# test file to check speed of checkPalindromeReverse function

import timeit

mysetup = '''
import random
from testarray_large import testArray
'''

mycode = '''
def countPalindromes(arr):
    count = 0
    for elem in arr:
        if(checkPalindromeReverse(elem)):
            count += 1
    return count

def checkPalindromeReverse(elem):
    elemReversed = elem[::-1]
    if(elem == elemReversed):
        return True
    else:
        return False

palindromesTotal = countPalindromes(testArray)
print("Total de palíndromos: %d " % palindromesTotal)
'''

print(timeit.timeit(setup = mysetup, stmt = mycode, number = 1))

# Output (using testarray.py)
# Total de palíndromos: 202 
# execution time = 0.002324899999999998

# Output (using testarray_large.py)
# Total de palíndromos: 0 
# execution time = 0.004580899999999999