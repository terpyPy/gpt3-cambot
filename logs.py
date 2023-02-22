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
        # decrypt the white_list, then encrypt the file again
        self.msg = message
        self.DBsec = DBsec
        self.DB_get = self.DBsec.read_encrypted_whitelist().split(sep='\n')
        self.admin = self.DB_get[0].strip('admin=')
        self.auth_users = self.DB_get[1].strip('auth_users=').split(sep=' ')

        self.session = {'chat_log': None,
                        'disc_auth': os.getenv('DISC_BOT_KEY'),
                        'API_access': True,
                        'ban_list': ['']}
        self.conMsg = 'DEFAULT'
        self.cmdLockout = False

    # takes the start time and returns the uptime in H:M:S.
    def uptime(self, startTime):
        uptime = time.time() - startTime
        uptime = time.strftime("%H:%M:%S", time.gmtime(uptime))
        return uptime

    def api_access(self, command):
        apiMsg = 'GPT3 api access is %sline' % command
        if command == 'on':
            self.session['API_access'] = True
            return apiMsg
        elif command == 'off':
            self.session['API_access'] = False
            return apiMsg

    def white_list(self, user):
        
        self.auth_users.append(str(user).strip())
        self.DBsec.write_encrypted_whitelist(
            f'admin={self.admin}\nauth_users=' + ' '.join(self.auth_users))
        print(self.admin, self.auth_users)

    def ban(self, user):
        self.auth_users.remove(str(user).strip())
        self.DBsec.write_encrypted_whitelist(
            f'admin={self.admin}\nauth_users=' + ' '.join(self.auth_users))
        print(self.admin, self.auth_users)
