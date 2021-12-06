class promopts:
    def __init__(self) -> None:
        engines = ["davinci-instruct-beta-v3", "davinci"]
        
        self.responsesLen = 64
        self.temp = float(0.9)
        self.top_p = float(1.0)
        
        self.Q_A_bot = {
            "start_sequence": "\nA:",
            "restart_sequence": "\n\nQ:",
            "session_prompt": "I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown",
            "engine": engines[1],
            "frequency_penalty": float(0),
            "presence_penalty": float(0)
            }
        
        self.Py_help_bot = {
            "start_sequence": "\nPython chatbot:",
            "restart_sequence": "\nYou: ",
            "session_prompt": "Python chatbot\n\n\nYou: How do I combine arrays?\nPython chatbot: You can use the extend() method.\nYou: How do I concatenate a list of strings to one string.\nPython chatbot: You can use the join() method.\nYou: how do I reshape arrays?\nPython chatbot: You can use the reshape() method.",
            "engine": engines[0],
            "frequency_penalty": float(0.5),
            "presence_penalty": float(0)
            }
        self.Py_explain = {
            "start_sequence": "\nPython chatbot:",
            "restart_sequence": "\nYou: ",
            "session_prompt": "#Python 3.7\n\n\n\n# Give an elaborate, high quality explanation for the above python code:\n\"\"\"",
            "engine": engines[0],
            "frequency_penalty": float(0.5),
            "presence_penalty": float(0)
            }