import time
from logs import Logs
class console(Logs):
    def __init__(self) -> None:
        super().__init__(self)
        # flag 0, is 0ff 1 is on
        self.flg = 1
        self.logs = Logs()
    def Consolecmd(self):
        inpt = input('disc_console>')
        if inpt:
            if inpt[0] == '+':
                Logs.white_list(self, inpt[2:])
            elif inpt[0] == '-':
                Logs.ban(self, inpt[2:])
            elif inpt.startswith("api"):
                cmd = inpt[4:]
                if (cmd == 'on') or (cmd == 'off'):
                    status = Logs.api_access(self,cmd)
                    print(status)
            
        # self.logs.conMsg = 'changed from cmd'   
    
    
    def main(self):            
        while True:
            self.Consolecmd()
            time.sleep(0.1)
            