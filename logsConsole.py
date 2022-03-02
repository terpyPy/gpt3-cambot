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
            elif inpt[0] == '-':
                self.logs.ban(inpt[2:])
            elif inpt.startswith("api"):
                cmd = inpt[4:]
                if (cmd == 'on') or (cmd == 'off'):
                    status = self.logs.api_access(cmd)
                    print(status)
                elif cmd.startswith("lockdown") or cmd == "-ld":
                    self.logs.cmdLockout = True       
                elif cmd.startswith("release") or cmd == "-r":
                    self.logs.cmdLockout = False       
            
   
        
    def main(self):            
        while True:
            self.Consolecmd()