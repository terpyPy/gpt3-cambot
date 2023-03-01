# !/usr/bin/python3
# 3/30/2022
# author: Cameron Kerley(terpy#3725)
# description: key string generator using cryptography module
from pathlib import Path
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv, set_key
import argparse
import zlib

load_dotenv('.env')

path = str(Path.cwd())+"\\"

class keyManger:
    def __init__(self,fileKey='.env'):
        self.isEncrypted = True
        # construct the path to .env file
        absoPath_fileKey = path + fileKey
        # check for the file in expected location
        if os.path.exists(absoPath_fileKey):
            # .env file exists, get the encryption key
            print(absoPath_fileKey, 'found')
            self.fileKey = os.getenv("fileKey")
        # error exists
        else:
            print("error: .env file not found")
        
        # if no secret key is provided then prompt to gen new secret.
        if not self.fileKey:
            # sanity check user input by capitalization
            prompt = input('Could not find key string fileKey create new key? (Y)es | (N)o:\n').capitalize()
            # in not yes prompt for valid input
            while (prompt[0] != 'Y'):
                # NO is a valid case, but will crash the bot if file is not plaintext
                if prompt[0] == 'N':
                    print('Warning continuing without valid Encryption/Decryption of resources!', __name__ , 'will encounter errors')
                    break
                else:
                    prompt = input('please respond Yes(y) | No(n): ').capitalize()
            # if yes gen a new secret   
            if prompt[0] == 'Y':
                self.fileKey = self._key_File_Generator(absoPath_fileKey)
                
    
    def _key_File_Generator(self,path):
        # key generation
        key = Fernet.generate_key()
        set_key(path, 'fileKey', key.decode('utf-8'))
        return os.getenv('fileKey')
    
    def encryptWhitelist(self):
        fernet = Fernet(self.fileKey)
        
        # opening the original file to encrypt
        with open(path + 'white_list.txt', 'rb') as file:
            original = file.read()
        
        # encrypting the file
        file.close()
        encrypted = fernet.encrypt(original)
        
        with open(path + 'white_list.txt', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        print('done encrypt')
        encrypted_file.close()
        self.isEncrypted = True
        
    def decryptWhitelist(self):
        fernet = Fernet(self.fileKey)
        
        # opening the encrypted file
        with open('white_list.txt', 'rb') as enc_file:
            encrypted = enc_file.read()
        
        # decrypting the file
        decrypted = fernet.decrypt(encrypted)
        enc_file.close()
        # opening the file in write mode and
        # writing the decrypted data
        with open('white_list.txt', 'wb') as dec_file:
            dec_file.write(decrypted)
        dec_file.close()
        print('done decrypt')
        self.isEncrypted = False
        
    def read_encrypted_whitelist(self):
        fernet = Fernet(self.fileKey)
        with open('white_list.txt', 'rb') as enc_file:
            encrypted = enc_file.read()
        enc_file.close()
        # print the crc32 checksum of the encrypted file
        print('crc32 checksum of encrypted file: ', zlib.crc32(encrypted))
        set_key('.env', 'last_read_crc32', str(zlib.crc32(encrypted)))
        decrypted = fernet.decrypt(encrypted)
        return decrypted.decode('utf-8')
        
    def write_encrypted_whitelist(self, data):
        fernet = Fernet(self.fileKey)
        encrypted = fernet.encrypt(data.encode('utf-8'))
        # print the crc32 checksum of the encrypted file
        print('crc32 checksum of encrypted file: ', zlib.crc32(encrypted))
        set_key('.env', 'last_write_crc32', str(zlib.crc32(encrypted)))
        with open('white_list.txt', 'wb') as enc_file:
            enc_file.write(encrypted)
        enc_file.close()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--mode',help='decrypt whitelist')
    t= keyManger()
    args = parser.parse_args()
 
    if args.mode== 'd':
        t.decryptWhitelist()
    if args.mode== 'e':
        t.encryptWhitelist()
    if args.mode== 'r':
        t._key_File_Generator('.env')
        print('done generation of new key')
    