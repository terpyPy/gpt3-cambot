from tokenGen.passtool import tools
class tokens:
    def __init__(self) -> None:
                               
        self.tools = tools()
        self.sessions = {'0': self.tools.getToken('test-Case'),
                         '1': self.tools.getToken('main-Session'),
                         '2': self.tools.getToken('test-new-chats'),
                         '3': self.tools.getToken('test-new-people'),
                         '4': self.tools.getToken('test-Web-Hooks'),
                         '5': self.tools.getToken('internal-app-seesion'),
                         }
        
if __name__ =='__main__':
    t = tokens()
    print(t.sessions['0'])
