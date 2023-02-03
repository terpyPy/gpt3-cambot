class promopts:
    def __init__(self) -> None:
        engines = ["code-davinci-001", "davinci"]
        
        self.responsesLen = 100
        self.temp = float(0.9)
        self.top_p = float(1.0)
        
        self.Q_A_bot = {
            "start_sequence": "\nA:",
            "restart_sequence": "\n\nQ:",
            "session_prompt": "I am a highly intelligent question answering bot. This is a chatbot on a discord server. This bot like to talk about topics including Machine Learning, Cybersecurity, cannabis research, chemistry, and ethics.\n\nQ: what is the mass of indole-3-butyric acid?\nA: the MW for indole-3-butyric acid is 203.2 g/mol.",
            "engine": "text-davinci-002",
            "frequency_penalty": float(0),
            "presence_penalty": float(0)
            }
        
        self.Py_help_bot = {
            "start_sequence": "\nPython chatbot:",
            "restart_sequence": "\nYou: ",
            "session_prompt": "this is a Python coding assistant. Python chatbot is an AI who is a python expert. it will awnser questions about or write python code.\nYou: write list comprehesion\nPython chatbot: [None for i in range(N)].",
            "engine": "text-davinci-002",
            "frequency_penalty": float(0.1),
            "presence_penalty": float(0)
            }
        self.Py_explain = {
            "start_sequence": "\n",
            "restart_sequence": "\n#",
            "session_prompt": "\nThis is a python devbot. Given a code comment,dev bot will produce accurate python3 code for each comment.\n#python3",
            "engine": engines[0],
            "frequency_penalty": float(0),
            "presence_penalty": float(0.1)
            }
        self.talkToBot = {
            "start_sequence": "\nbot:",
            "restart_sequence": "\ncomment:",
            "session_prompt": "This is a chatbot on a discord server. This bot like to talk about topics including Machine Learning, Cybersecurity, cannabis research, chemistry, and ethics. This bot responds to Nonsense and explicate messages with \"Sorry I don't understand\".",
            "engine": "text-davinci-002",
            "frequency_penalty": float(0.45),
            "presence_penalty": float(0.4)
            }
        self.promptArray = [self.Q_A_bot, self.Py_explain,self.Py_help_bot,self.talkToBot]
    def createTopDict(self):
        # Create top level dictionary with,Q_A_bot, py_help_bot, Py_explain and spreadsheet,
        # as values in the top level dictionary called topDict.
        topDict = {}
        keyNameSpace = ['QA','py','test','talk']
        for i in range(len(self.promptArray)):
            topDict[keyNameSpace[i]] = self.promptArray[i]
        return topDict

if __name__ == '__main__':
    d = promopts() 
    t = d.createTopDict()
    print(t)