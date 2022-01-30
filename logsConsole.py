
class console:
    def __init__(self,session) -> None:
        super().__init__()
        # flag 0, is 0ff 1 is on
        self.flg = 1
        self.session = session
    def Consolecmd(self):
        inpt = input('disc_console>')
        if inpt:
            if inpt[0] == '+':
                self.white_list(inpt[2:])
            elif inpt[0] == '-':
                self.ban(inpt[2:])
            elif inpt.startswith("api"):
                if inpt[4:] == 'on':
                    self.session['API_access'] = True
                if inpt[4:] == 'off':
                    self.session['API_access'] = False
                    
            else:
                print("invalid")
def main(sessh):            
    eh = console(sessh)
    while True:
        eh.Consolecmd()