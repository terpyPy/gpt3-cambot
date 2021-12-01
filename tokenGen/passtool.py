#!/usr/bin/python3
#
#  Author:      Cameron Kerley
#  Date:        23 Feb 2020
#  Description: password tool run file
from . import allTheFuctions
import math
import logging



class tools:
    def __init__(self) -> None:
        self.keyDivisor = 91

    def getToken(self, password):
    
        key = len(password)  # 1.1 get variable key
        #
        # math.sqrt() is a better logic for block encrypted strings
        while key >= self.keyDivisor:
            key = round(math.sqrt(key))
        #
        # layer one calculated key string, store the block encrypted txt string
        # scrambles the txt given the key previous, this is point of cipher origan for symbols in LETTERS
        scram = (allTheFuctions.ceaser(key,password ))
        scram = (allTheFuctions.encryptMessage(key, scram))
        logging.info('[hash]:--- ', scram, '\n')
        return scram

    def decryption(self, encryptPass):
        #
        # get the legnth of the keystring
        key = len(encryptPass)  

        while key >= self.keyDivisor:
            key = round(math.sqrt(key))

        # decrypt layer one calculated key string, store the still block encrypted txt string
        unScram = allTheFuctions.ceaserUndo(key, encryptPass)
        # with the given key decode the string position
        unScram = allTheFuctions.decryptMessage(key, unScram)
        logging.info('[removed sudo hash]:---- ', unScram)
        return unScram

    if __name__ =='__main__':
        getToken('this_is!aTest')
