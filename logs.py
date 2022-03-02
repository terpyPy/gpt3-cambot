import os
import re
import time
class Logs():
    def __init__(self, message=None):
        DB_get = self.read_whitelist()
        self.admin = DB_get[0]
        self.msg = message
        self.auth_users = DB_get[1]

        self.session = {'chat_log': None,
                        'disc_auth': os.getenv('DISC_BOT_KEY'),
                        'API_access': True,
                        'ban_list': ['']}
        self.conMsg = 'DEFAULT'
        self.cmdLockout = False
        
    def uptime(self,startTime,hours):
        runtimeMin = (time.time() - startTime) // 60
        sec = (time.time() - startTime)
        if sec >= 60:
            sec %=60
        if runtimeMin >= 60:
            hours += 1
            runtimeMin %= 60
        H_M_S_time = ('Hours ' +str(hours)+ ' : ' + str(round(runtimeMin)) + ' : ' + str(round(sec)))
        return H_M_S_time
    
        
    def api_access(self, command):
        apiMsg = 'GPT3 api access is %sline' %command
        if command == 'on':
            self.session['API_access'] = True
            return apiMsg
        elif command == 'off':
            self.session['API_access'] = False
            return apiMsg
    def read_whitelist(self):
        # this function parses the whitlist to config out init variables
        white_list = open('white_list.txt')
        fileLines = white_list.readlines()
        white_list.close()
        # regular expersions to search for admin= and auth_users=
        adminRE = re.compile(r'^a\w[a-z]{1,}=(.*)')
        authUserRE = re.compile(r'^a\w[a-z]{1,}_.*=(.*)')
        admin = ''
        authUsers = ''
        for line in fileLines:
            if adminRE.search(line):
                admin = adminRE.search(line)
            elif authUserRE.search(line):
                authUsers = authUserRE.search(line)
        # return the admin as and the users string ling as a list
        return str(admin.groups()[0]), authUsers.groups()[0].split(sep=' ')
    
    def DB_update(self):
        DB_get = self.read_whitelist()
        self.admin = DB_get[0]
        self.auth_users = DB_get[1]
        print(self.admin, self.auth_users)
        
    def white_list(self,user):
        self.auth_users.append(str(user))
        with open('white_list.txt', 'w') as f:
            for line in ['admin='+self.admin+'\n', 'auth_users=' + ' '.join(self.auth_users)]:
                f.write(line)
        self.DB_update()
        
    def ban(self,user):
        self.auth_users.remove(str(user))
        with open('white_list.txt', 'w') as f:
            for line in ['admin='+self.admin+'\n', 'auth_users=' + ' '.join(self.auth_users)]:
                f.write(line)
        self.DB_update()
    
    async def hook(self,message):
        await message.channel.send(self.conMsg)