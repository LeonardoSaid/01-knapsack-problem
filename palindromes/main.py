# Author: Leonardo Said
# GitHub: https://github.com/LeonardoSaid/
# Problem: For an array with 10k strings where each string contains either 3 or 5 characters, count how many of those strings are palindromes.
# Problema: Para uma array com 10.000 strings com 3 ou 5 caracteres, contar quantas strings são palíndromos.

import random

# generateTestArray(arraySize: number, elemLength: number[]) : string[]
# Generates an array of size 'arraySize' where each element is a string of a random length in 'elemLength' array
# Example: generateTestArray(10000, [3,5]) returns an array with 10000 strings where each string is 3 or 5 characters long
def generateTestArray(arraySize, elemLength):
    return [randomString(random.choice(elemLength)) for i in range(arraySize)]

# randomString(n: number) : string
# returns a random string of size 'n' composed of A-Z characters
def randomString(n):
    result = []
    for _ in range(n):
        randomNumber = 65 + random.randint(0, 25)
        result.append(chr(randomNumber))
    return ''.join(result)

# countPalindromes(arr : string[]) : number
# returns the total number of string palindromes in a given array of strings
def countPalindromes(arr):
    count = 0
    for elem in arr:
        if(checkPalindromeReverse(elem)):
            count += 1
    return count

# checkPalindromeReverse(elem : string) : boolean
# checks if a string is a palindrome by comparing the original with its reversed form
def checkPalindromeReverse(elem):
    elemReversed = elem[::-1]
    if(elem == elemReversed):
        return True
    else:
        return False

# checkPalindrome(elem : string) : boolean
# checks if a string is a palindrome by comparing mirrored characters (first character with the last and so on)
def checkPalindrome(elem):
    length = len(elem)
    for i in range(0, length // 2 + 1):
        if(elem[i] != elem[length-i-1]):
            return False
    return True

# main
testArray = generateTestArray(10000, [3, 5])
palindromesTotal = countPalindromes(testArray)
print("Total de palíndromos: %d " % palindromesTotal)