import os
import openai
from dotenv import load_dotenv
from random import choice
from flask import Flask, request

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nCambot:"
restart_sequence = "\nHuman: "
session_prompt = "The following is a conversation with an AI named Cambot. Cambot is creative, clever, and only speaks in riddles.\n\nHuman: Hello, who are you?\nCambot: I am  Cambot. How can I help you today?\nHuman: "

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_text,
        temperature=0.9,
        max_tokens=120,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
        )
    text = response['choices'][0]['text']
    return str(text)

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None: 
        chat_log = session_prompt 
        return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'