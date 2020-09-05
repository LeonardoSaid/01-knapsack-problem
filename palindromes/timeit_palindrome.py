# test file to check speed of checkPalindrome function

import timeit

mysetup = '''
import random
from testarray_large import testArray
'''

mycode = '''
def countPalindromes(arr):
    count = 0
    for elem in arr:
        if(checkPalindrome(elem)):
            count += 1
    return count

def checkPalindrome(elem):
    length = len(elem)
    for i in range(0, length // 2 + 1):
        if(elem[i] != elem[length-i-1]):
            return False
    return True
    
palindromesTotal = countPalindromes(testArray)
print("Total de palíndromos: %d " % palindromesTotal)
'''

print(timeit.timeit(setup = mysetup, stmt = mycode, number = 1))

# Output (using testarray.py)
# Total de palíndromos: 202 
# execution time = 0.005405300000000002

# Output (using testarray_large.py)
# Total de palíndromos: 0 
# execution time = 0.006227100000000013