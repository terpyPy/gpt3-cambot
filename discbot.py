import threading
import discord
from discord.ext import commands
from chatBot import append_interaction_to_chat_log, ask
from logs import Logs
import logsConsole
import time

logs = Logs()
startTime = time.time()
hours = 0
intents = discord.Intents.default()
client = commands.Bot(command_prefix='$', intents=intents.all())
cmd = logsConsole.console(logs)
thread1 = threading.Thread(target=cmd.main,
                           args=(), daemon=True)


@client.event
async def on_ready():
    cmd.flg = 0
    # let yourclient know when the bot is ready to be propmeted on startup
    print('Logged on as {0}!'.format(client.user))


@client.event
async def on_message(message):
    if not logs.cmdLockout:

        # prevent the bot from using or echoing commands it sends
        if message.author == client.user:
            return

        if message.content.startswith('$'):
            cmd.flg = 0
            # check the temp ban list stored in memory
            if not str(message.author) in logs.session['ban_list']:
                await client.on_command_anyone(message)
            else:
                await message.channel.send(str(message.author) + ' is ban')
            # if not ban and the command is whitelist scope check if user is whitelisted
            if (str(message.author) in logs.auth_users):
                await client.on_command_API(message)
            else:
                await message.channel.send(
                    'please ask ' + logs.admin + ' to be whitelisted these questions cost money')
            # check if the user is admin and if so  check if the command is admin scope
            if (str(message.author) == logs.admin):
                await client.privileged_command(message)


@client.event
async def on_command_anyone(message):
    if message.content.startswith('$he') or message.content.startswith('$?'):
        answer = ('usage:',
                  '\n$QA [your question],',
                  '\n$py [question about programming],',
                  '\n$reset: this resets prompt and memory',
                  '\n$ping: ping the server',
                  '\n$uptime: uptime of the bot',)

        print(message.author, 'on_command_whitelisted')
        await message.channel.send(' '.join(answer))
        
    elif message.content.startswith('$ping'):
        print(message.author, 'on_command_whitelisted')
        await message.channel.send(f"Pong! {round(client.latency * 1000)}ms")

    elif message.content.startswith('$uptime'):
        upTime = logs.uptime(startTime)
        await message.channel.send(upTime)


@client.event
async def on_command_API(message):
    # OpenAI bot commands, only whitelisted users can prompt the bot and reset the prompt history
    cmd_keys = map(lambda x: f'${x}', logs.API_CMDS)
    cmd_dict = dict(zip(cmd_keys, logs.API_CMDS))

    if logs.session['API_access']:
        # OpenAI bot commands
        # 0: q&a
        # 1: py
        # 2: reset
        #
        # check the message for just the command
        cmd = message.content[:message.content.find(' ')]

        if cmd_dict.get(cmd):
            print(message.author, f'on_command_API_{cmd_dict.get(cmd)}')
            ans = get_awnser(message, cmd[1:])
            await message.channel.send(ans)

        elif message.content.startswith('$re'):
            await message.channel.send("conversation and respones cache cleared.")
            print(message.author, 'on_command_API_reset')

    elif not logs.session['API_access'] and str(message.content)[:3] in logs.API_CMDS:
        await message.channel.send('api access is unavailable contact ' + logs.admin)


@client.event
async def privileged_command(message):
    # admin scope check & auto ban for attempted use,
    #
    # check the message for just the command
    is_command = message.content.startswith('$GPT3 ')

    if is_command:
        # parse the message for just the command
        command = message.content[6:]
        print(message.author, 'privileged_command', '$GPT3')
        content = admin_options(command)
        await message.channel.send(content)

# ---------------------- non-async functions/handlers ---------------------- #

def ban(command):
    # ban a user from using the bot
    user = command.split(sep=' ')[1]
    logs.session['ban_list'].append(str(user))
    logs.ban(user)
    return str(user) + ' removed from white-list and ban from $ commands'


def white_list(command):
    # add a user to the whitelist
    user = command.split(sep=' ')[1]
    logs.white_list(user)
    return str(user) + ' white-listed for GPT3 API'


def admin_options(command):
    # admin privilege commands
    logs.ADMIN_CMDS = ['on', 'off', '+', '-']
    funcs_list = [logs.api_access, logs.api_access, white_list, ban]
    options_dict = dict(zip(logs.ADMIN_CMDS, funcs_list))
    # normalize the command with a space 
    cmd = command + ' '
    cmd = cmd[:int(cmd.find(' '))]
    # GPT 3 api access control
    if cmd in logs.ADMIN_CMDS:
        status = options_dict[cmd](command)
        return status

    else:
        return 'options are [on] or [off], \nrecived invalid : ' + command


def get_awnser(message, command='QA'):
    # parse input to exclude $identifier
    incoming_msg = message.content[4:]
    # get chat log and then,
    chat_log = logs.session['chat_log']
    # ask question with incoming message and chat log
    answer = ask(incoming_msg, chat_log, prompt_type=command)
    # add both entry's to the chatlog
    logs.session['chat_log'] = append_interaction_to_chat_log(incoming_msg,
                                                              answer,
                                                              chat_log,
                                                              prompt_type=command
                                                              )
    # print(logs.session['chat_log'])
    return answer


if __name__ == '__main__':
    thread1.start()
    client.run(logs.session['disc_auth'])
