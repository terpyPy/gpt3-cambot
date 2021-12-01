import os
import openai
from dotenv import load_dotenv
from random import choice
from flask import Flask, request

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nFriend:"
restart_sequence = "You: "
session_prompt = "You: Yoo waz up?\nFriend: About to start my twitch stream.\nYou: Word, playing some games?\nFriend: Naw, probably just chatting and youtube videos tonight.\nYou: "

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_text,
        temperature=0.4,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.15,
        stop=["You:"]
        )
    text = response['choices'][0]['text']
    return str(text)

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None: 
        chat_log = session_prompt 
        return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'