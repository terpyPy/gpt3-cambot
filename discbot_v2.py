import threading
import discord
from discord.client import Client
from chatBot import append_interaction_to_chat_log, ask
from tokenGen.passtool import tools
from logs import Logs
import logsConsole

logs = Logs()
hasher = tools()

client = discord.Client()