import os
import openai
from prompt_tools import promopts

openai.api_key = os.getenv("OPENAI_API_KEY")

settings = promopts()
qa = settings.Q_A_bot
py_help = settings.Py_help_bot

tasks_dict = {'QA': qa,
              'py': py_help}


def ask(question, chat_log=None, prompt_type='QA'):
    restart_sequence, start_sequence, engine_type, session_prompt,f_pen,p_pen = getSettings(prompt_type)
    prompt_text = f'{chat_log}{restart_sequence}:{question}{start_sequence}:'
    response = openai.Completion.create(
        engine=engine_type,
        prompt=prompt_text,
        temperature=settings.temp,
        max_tokens=64,
        top_p=settings.temp,
        frequency_penalty=f_pen,
        presence_penalty=p_pen,
        stop=["\n"]
    )
    text = response['choices'][0]['text']
    return str(text)


def getSettings(type_p):

    return (tasks_dict[type_p]['restart_sequence'],
            tasks_dict[type_p]["start_sequence"],
            tasks_dict[type_p]["engine"],
            tasks_dict[type_p]["session_prompt"],
            tasks_dict[type_p]['frequency_penalty'],
            tasks_dict[type_p]['presence_penalty'])


def append_interaction_to_chat_log(question, answer, chat_log=None, prompt_type='QA'):
    restart_sequence, start_sequence, engine_type, session_prompt,f,p = getSettings(
        prompt_type)
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
