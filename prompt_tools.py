import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class completion_tasks:
    def __init__(self) -> None:
        self.stop_type = [None, ["\"\"\""]]
        self.audience = ''
        self.topic = str(input('Audience to complet with: '))
        self.prompt = "The sensations of Pabodie and myself at receipt of this report were almost beyond description, nor were our companions much behind us in enthusiasm. McTighe, who had hastily translated a few high spots as they came from the droning receiving set, wrote out the entire message from his shorthand versionas soon as Lake's operator signed off. All appreciated the epoch-making significance of the discovery, and I sent Lake congratulations as soon as the Arkham's operator had repeated back the descriptive parts as requested; and my example was followed by Sherman from his station at the McMurdo Sound supply cache, as well as by Captain Douglas of the Arkham. Later, as head of the expedition, I added some remarks to be relayed through the Arkham to the outside world. Of course, rest was an absurd thought amidst this excitement; and my only wish was to get to Lake's camp as quickly as I could. It disappointed me when he sent word that a rising mountain gale made early aerial travel impossible."
        
        self.explain_code = "\n\n\"\"\"\nHere's what the above function is doing:\n1.",
        self.write_a_paragraph = "Write a paper about, " + self.topic + ".\nIntroduction: inform the reader briefly about " + self.topic + ".\n\n" + self.prompt + "\n\nBody Paragraph: inform the reader about " + self.topic + " and it's limitations.\n\n"
        self.summarize = "A " + self.audience + " asked me what this information means:\n\"\"\"\n" + self.prompt + "\n\"\"\"\n\nI analogized it in language " + self.audience + " would use:\n\"\"\"\n"
        
        # "There’s an old saying from network security admins that goes “The weakest link in any computer system is a person”. This saying isn’t meant to suggest that computers are infallible or smarter than humans. If you gauge intelligence purely by computational ability, a 50-cent calculator is smarter than any Human to exist. I believe this saying means, a computer is an incredibly powerful tool, but like all tools it is bottlenecked by human ingenuity and innovation or lack thereof. As such, the AI of today and tomorrow is limited by the sum of our best efforts to make it a reality. A computer doesn’t decide to innovate or optimize, it simply waits for a human to tell it how and when"
        
        # 0 is no audience 1 is no topic,
        self.tasks = [self.write_a_paragraph,
                      self.summarize,
                      self.explain_code
                                            ]
        
        # task flag
        self.task_type = 0

def get_task(request):
    if request.topic == '':
        task_end = request.stop_type[1]
        task = request.tasks[1]

    else:
        task_end = request.stop_type[0]
        task = request.tasks[0]
    return task,task_end

options = completion_tasks()
task, task_end = get_task(options)
response = openai.Completion.create(
    engine="davinci",
    prompt= task,
    temperature=0,
    max_tokens=105,
    top_p=1,
    # best_of=1,
    frequency_penalty=0,
    presence_penalty=0.03,
    stop=task_end
)
output = response.choices[0].get("text")
print(task,'\n' + 'your competion:\n' + output, '\n',task_end)
