#!/usr/bin/python3
#
#  Author:      Cameron Kerley
#  Date:        16 March 2019
#  Description: ideas for more functions source code
import math



##########################################################################################################
# Description: Transposition Cipher Encryption
# Each string in ciphertext represents a column in the grid.
# Convert the ciphertext list into a single string value and return it.
##########################################################################################################
def encryptMessage(key, message):
    # Each string in ciphertext represents a column in the grid.
    ciphertext = [''] * key

    # Loop through each column in ciphertext.
    for col in range(key):
        pointer = col

        # Keep looping until pointer goes past the length of the message.
        while pointer < len(message):
            # Place the character at pointer in message at the end of the
            # current column in the ciphertext list.
            ciphertext[col] += message[pointer]

            # move pointer over
            pointer += key

    #print(ciphertext)
    return ''.join(ciphertext)


# Transposition Cipher Decryption
def decryptMessage(key, message):
    # The transposition decrypt function will simulate the "columns" and
    # "rows" of the grid that the plaintext is written on by using a list
    # of strings. First, we need to calculate a few values.

    # The number of "columns" in our transposition grid:
    numOfColumns = key
    # The number of "rows" in our grid will need:
    numOfRows = math.ceil(len(message)/key)
    # The number of "shaded boxes" in the last "column" of the grid:
    numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)

    # Each string in plaintext represents a column in the grid.
    plaintext = [''] * numOfColumns

    # The col and row variables point to where in the grid the next
    # character in the encrypted message will go.
    col = 0
    row = 0

    for symbol in message:
        plaintext[col] += symbol
        col += 1  # point to next column

        # If there are no more columns OR we're at a shaded box, go back to
        # the first column and the next row.
        if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
            col = 0
            row += 1
    #print(plaintext, '\n')
    return ''.join(plaintext)

##########################################################################################################
#  Description: Caesar Cipher
# the string to be encrypted/decrypted
# stores the encrypted/decrypted form of the message
##########################################################################################################


def ceaser(key, message):
    mode = 'encrypt'  # set to 'encrypt' or 'decrypt'
    # every possible symbol that can be encrypted
    LETTERS = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz~'
    translated = ''
    # run the encryption/decryption code on each symbol in the message string
    for symbol in message:
        # TODO: math.gcd is a better logic
        if symbol in LETTERS:
            # get the encrypted (or decrypted) number for this symbol
            num = LETTERS.find(symbol)
            num = num + key
            # handle the wrap-around if num is larger than the length of LETTERS or less than 0
            totalKeys = len(LETTERS) - 1
            while num >= totalKeys:
                num = num - totalKeys
            if num < 1:
                num = num + totalKeys

            # add encrypted/decrypted number's symbol at the end of translated
            translated = translated + LETTERS[num]
        else:
            # just add the symbol without encrypting/decrypting
            translated = translated + symbol

    # print the encrypted/decrypted string to the screen
    return translated


def ceaserUndo(key, message):
    mode = 'decrypt'
    # every possible symbol that can be encrypted
    LETTERS = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz~'
    translated = ''
    # run the encryption/decryption code on each symbol in the message string
    for symbol in message:
        if symbol in LETTERS:
            # get the encrypted (or decrypted) number for this symbol
            num = (LETTERS.find(symbol))  # get the number of the symbol
            num = (num - int(key))

            totalKeys = len(LETTERS) - 1
            while num >= totalKeys:
                num = num - totalKeys
            if num < 1:
                num = num + totalKeys

            # add encrypted/decrypted number's symbol at the end of translated
            translated = (translated + LETTERS[num])

        else:
            # just add the symbol without encrypting/decrypting
            translated = (translated + symbol)

    # print the encrypted/decrypted string to the screen
    return translated


#########################################################################################################
def reversePrint(intStr):
    # revInt will hold the output for our new string
    revIntStr = ''
    index = len(intStr)
    while index > 0:
        revIntStr += intStr[index - 1]
        index = index - 1
    return revIntStr


##########################################################################################################
'''find the most commen element by making the list an irt set and count occurrences fo each ele
then max the set of occurrencesget the largest and find its index in oldlist
return the elem of that index, then given the common ele enumerate the list while adding 
all elements not commen to thenew list return value'''
##########################################################################################################


def removeElement(oldList: list):
    newList = []
    mostCommenEle = max(set(oldList), key=oldList.count)
    for pos, var in enumerate(oldList):
        if oldList[pos] == mostCommenEle:
            continue
        else:
            newList += [var]
    totalRemoved = len(oldList) - len(newList)
    return newList, totalRemoved, mostCommenEle


def main():
    print('import only')


if __name__ == '__main__':
    main()
