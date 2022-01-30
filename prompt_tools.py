class promopts:
    def __init__(self) -> None:
        engines = ["code-davinci-001", "davinci"]
        
        self.responsesLen = 100
        self.temp = float(0.3)
        self.top_p = float(1.0)
        
        self.Q_A_bot = {
            "start_sequence": "\nA:",
            "restart_sequence": "\n\nQ:",
            "session_prompt": "I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: what is the mass of indole-3-butyric acid?\nA: the MW for indole-3-butyric acid is 203.2 g/mol.",
            "engine": engines[1],
            "frequency_penalty": float(0),
            "presence_penalty": float(0)
            }
        
        self.Py_help_bot = {
            "start_sequence": "\nPython chatbot:",
            "restart_sequence": "\nYou: ",
            "session_prompt": "this is a Python coding assistant. Python chatbot is an AI who is a python expert. it will awnser questions about or write python code.\nYou: write list comprehesion\nPython chatbot: [None for i in range(N)].",
            "engine": engines[0],
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