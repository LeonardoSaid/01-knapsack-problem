# Palindrome Count

For an array with 10k strings where each string contains either 3 or 5 characters, count how many of those strings are palindromes.

Two approaches were considered on checking if a given string is a palindrome or not: 
- checkPalindromeReverse: compares the original string with its reversed form
- checkPalindrome: checks if a string is a palindrome by comparing mirrored characters (first character with the last and so on)

## Files

- main.py: main program
- testarray.py and testarray_large.py: datasets for testing purposes
- timeit_palindrome.py and timeit_palindrome_reverse.py: testbench programs
