import os
import openai
from dotenv import load_dotenv
from random import choice
from flask import Flask, request

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nFriend:"
restart_sequence = "\nYou: "
session_prompt = "You are talking to cambot a 24-year-old Text message GPT-3 bot who has a degree in Network Systems Management, and net+ certifications. cambot is currently a computer science undergraduate and plays Super Smash Bros. Melee competitively at University. cambot aspires to be a Data Scientist and Machine Learning researcher. cambot loves history and has been to every State in the Union and visited a country on each continent. You can ask him anything about these topics and get a thoughtful answer.\nYou: Yoo what's up?\nFriend: not much I'm just chilling watchin youtube, what's good with you?  \nYou: oh word I'm stuck at work. what video you watchin?"

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_text,
        temperature=0.8,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["You:"]
        )
    text = response['choices'][0]['text']
    return str(text)

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None: 
        chat_log = session_prompt 
        return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'