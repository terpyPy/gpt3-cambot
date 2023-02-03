import os
import re
import time
from tokenGen import fKey
import discord

DBsec = fKey.keyManger()
if not DBsec.isEncrypted:
    DBsec.encryptWhitelist()
    DBsec.isEncrypted = True
    
class Logs():
    def __init__(self, message=None):
        #decrypt the white_list, then encrypt the file again
        self.DBsec = DBsec
        self.DBsec.decryptWhitelist()
        DB_get = self.read_whitelist()
        self.DBsec.encryptWhitelist()
        
        self.admin = DB_get[0]
        self.msg = message
        self.auth_users = DB_get[1]

        self.session = {'chat_log': None,
                        'disc_auth': os.getenv('DISC_BOT_KEY'),
                        'API_access': True,
                        'ban_list': ['']}
        self.conMsg = 'DEFAULT'
        self.cmdLockout = False
        
        
    # takes the start time and returns the uptime in H:M:S.
    def uptime(self,startTime):
        uptime = time.time() - startTime
        uptime = time.strftime("%H:%M:%S", time.gmtime(uptime))
        return uptime
        
    
        
    def api_access(self, command):
        apiMsg = 'GPT3 api access is %sline' %command
        if command == 'on':
            self.session['API_access'] = True
            return apiMsg
        elif command == 'off':
            self.session['API_access'] = False
            return apiMsg
        
        
    def read_whitelist(self):
        '''this function parses the whitelist to get admin and auth_users,
        and returns a tuple of the two(str, list)'''
        white_list = open('white_list.txt')
        fileLines = white_list.readlines()
        white_list.close()
        # create regular expressions to search for "admin=" and "auth_users=" called "adminRE" and "authUserRE"
        adminRE = re.compile(r'^a\w[a-z]{1,}=(.*)')
        authUserRE = re.compile(r'^a\w[a-z]{1,}_.*=(.*)')
        # search for adminRE and authUserRE in fileLines
        admin = adminRE.search(fileLines[0])
        authUsers = authUserRE.search(fileLines[1])
        # return the admin and authUsers as a tuple
        return f"{admin.groups()[0]}", authUsers.groups()[0].split(sep=' ')
    
    
    def DB_update(self):
        DB_get = self.read_whitelist()
        self.admin = DB_get[0]
        self.auth_users = DB_get[1]
        print(self.admin, self.auth_users)
       
        
    def white_list(self,user):
        self.DBsec.decryptWhitelist()
        self.auth_users.append(str(user))
        with open('white_list.txt', 'w') as f:
            for line in ['admin='+self.admin+'\n', 'auth_users=' + ' '.join(self.auth_users)]:
                f.write(line)
        f.close()
        self.DB_update()
        self.DBsec.encryptWhitelist()
      
        
    def ban(self,user):
        self.DBsec.decryptWhitelist()
        self.auth_users.remove(str(user))
        with open('white_list.txt', 'w') as f:
            for line in ['admin='+self.admin+'\n', 'auth_users=' + ' '.join(self.auth_users)]:
                f.write(line)
        f.close()
        self.DB_update()
        self.DBsec.encryptWhitelist()
        