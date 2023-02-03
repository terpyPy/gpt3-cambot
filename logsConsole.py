class console:
    def __init__(self,logs) -> None:
        # flag 0, is 0ff 1 is on
        self.flg = 1
        self.logs = logs
    def Consolecmd(self):
        inpt = input('disc_console>')
        
        if inpt:
            
            if inpt[0] == '+':
                self.logs.white_list(inpt[2:])
                return
                
            elif inpt[0] == '-':
                self.logs.ban(inpt[2:])
                return
            
            elif inpt.startswith("api"):
                # 
                cmd = inpt[4:]
                if (cmd == 'on') or (cmd == 'off'):
                    status = self.logs.api_access(cmd)
                    print(status)
                    return
                    
                elif cmd.startswith("lockdown") or cmd == "-ld":
                    self.logs.cmdLockout = True
                    print(f'console level lockout on bot function {self.logs.cmdLockout}')   
                    return
                
                elif cmd.startswith("release") or cmd == "-r":
                    self.logs.cmdLockout = False
                    print(f'console level lockout on bot function {self.logs.cmdLockout}')
                    return
            elif inpt.startswith('encrypt'):
                currFlag = self.logs.DBsec.isEncrypted
                if not currFlag:
                    self.logs.DBsec.encryptWhitelist()
                    return
                else:
                    print(f'logs could not encrypt \nDBsec.isEncrypted: {currFlag}')
                    
                   
            elif inpt.startswith('decrypt'):
                currFlag = self.logs.DBsec.isEncrypted
                if currFlag:
                    self.logs.DBsec.decryptWhitelist()
                    print('MUST BE ENCRYPTED TO RUN BOT!!!! PLEASE DO "api -ld" to prevent crash')
                    return
                else:
                    print(f'logs could not decrypt \nDBsec.isEncrypted: {currFlag}')
    def main(self):            
        while True:
            self.Consolecmd()
            