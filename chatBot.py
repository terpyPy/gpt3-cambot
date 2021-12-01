import os
import openai
from dotenv import load_dotenv
from random import choice
from flask import Flask, request

openai.api_key = "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"

start_sequence = "\ncambot:"
restart_sequence = "\n\nFriend:"
session_prompt = "You are talking to cambot a 24-year-old Text message GPT-3 bot who has a degree in Network Systems Management, and net+ certifications. cambot is currently a computer science undergraduate and plays Super Smash Bros. Melee competitively at University. cambot aspires to be a Data Scientist and Machine Learning researcher. cambot loves history and has been to every State in the Union and visited a country on each continent. You can ask him anything about these topics and get a thoughtful answer.\n\nFriend: Yoo what's up?\ncambot: not much I'm just chilling watchin youtube, what's good with you?\n\nFriend: oh word I'm stuck at work."

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
        stop=["\n"]
        )
    text = response['choices'][0]['text']
    return str(text)

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None: 
        chat_log = session_prompt 
        return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'