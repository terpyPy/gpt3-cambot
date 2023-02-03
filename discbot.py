import threading
import discord
from discord.ext import commands
from chatBot import append_interaction_to_chat_log, ask
from tokenGen.passtool import tools
from logs import Logs
import logsConsole
import time
intents = discord.Intents.default()

logs = Logs()
startTime = time.time()
hours = 0
hasher = tools()
client = commands.Bot(command_prefix='$', intents=intents.all())
cmd = logsConsole.console(logs)
thread1 = threading.Thread(target=cmd.main,
                           args=(), daemon=True)


@client.event
async def on_ready():
    # let yourclient know when the bot is ready to be propmeted on startup
    print('Logged on as {0}!'.format(client.user))


@client.event
async def on_message(message):
    if not logs.cmdLockout:

        # prevent the bot from using or echoing commands it sends
        if message.author == client.user:
            return

        if message.content.startswith('$'):
            # check the temp ban list stored in memory
            if not str(message.author) in logs.session['ban_list']:
                await client.on_command_anyone(message)
                # if not ban and the command is whitelist scope check if user is whitelisted
                if (str(message.author) in logs.auth_users):
                    await client.on_command_API(message)
                    await client.privileged_command(message)

                else:
                    await message.channel.send(
                        'please ask ' + logs.admin + ' to be whitelisted these questions cost money')
            else:
                await message.channel.send(str(message.author) + ' is ban')


@client.event
async def on_command_anyone(message):
    if message.content.startswith('$he') or message.content.startswith('$?'):
        answer = ('usage:',
                  '\n$QA [your question],',
                  '\n$py [question about programing],',
                  '\n$reset: this resets prompt and memory',
                  '\n$ping: ping the server',
                  '\n$fakehash: scramble a phrase',
                  '\n$fakehash-d: decrypt the phrase',
                  '\n$streamerMode: fuck around and find out')

        print(message.author, 'on_command_whitelisted')
        await message.channel.send(' '.join(answer))


    elif message.content.startswith('$hook'):
        await logs.hook(message)

    elif message.content.startswith('$fakehash'):
        incoming_phrase = message.content[9:]
        h = hasher.getToken(incoming_phrase)
        print(message.author, 'on_command_whitelisted')
        await message.channel.send(h)

    elif message.content.startswith('$fakehash-d '):
        incoming_phrase = message.content[11:]
        h = hasher.decryption(incoming_phrase)
        print(message.author, 'on_command_whitelisted')
        await message.channel.send(h)

    elif message.content.startswith('$ping'):
        print(message.author, 'on_command_whitelisted')
        await message.channel.send(f"Pong! {round(client.latency * 1000)}ms")

    elif message.content.startswith('$uptime'):
        upTime = logs.uptime(startTime)
        await message.channel.send(upTime)



@client.event
async def on_command_API(message):
    # OpenAI bot commands, only whitelisted users can propmet the bot and reset the propmet history
    commands = ('$QA', '$py', '$re')
    if logs.session['API_access']:
        # OpenAI bot commands
        # 0: q&a
        # 1: py
        # 2: reset
        if message.content.startswith(commands[0]):
            answer = get_awnser(message, 'QA')
            await message.channel.send(answer)
            print(message.author, 'on_command_API')

        elif message.content.startswith(commands[1]):
            answer = get_awnser(message, 'py')
            await message.channel.send(answer)
            print(message.author, 'on_command_API')

        elif message.content.startswith(commands[2]):
            await message.channel.send("conversation and respones cache cleared.")
            print(message.author, 'on_command_API')

    elif not logs.session['API_access'] and str(message.content)[:3] in commands:
        await message.channel.send('api access is unavailable contact ' + logs.admin)


@client.event
async def privileged_command(message):
    # admin scope check & auto ban for attempted use,
    #
    # check the message for just the command
    is_command = message.content.startswith('$GPT3 ')

    if (str(message.author) == logs.admin):

        if is_command:
            print(message.author, 'privileged_command')

            # parse the message for just the command
            command = message.content[6:]
            print(command)
            await client.admin_options(command, message)

    if not (str(message.author) == logs.admin) and is_command:
        # auto ban users that attempt to use admin scope commands, also removes from whitelist if present.
        logs.session['ban_list'].append(str(message.author))
        logs.ban(str(message.author))

        await message.channel.send(
            '@' + str(message.author) + ' you\'re attempt to use privilege commands has notified ' + logs.admin + '\nyour privileges and whitelist are revoked , and the attempt was logged')


@client.event
async def admin_options(command, message):
    # admin privilege commands
    #
    # GPT 3 api access control
    truthTable = ('on' or 'off')
    if command == truthTable:
        status = logs.api_access(command)
        await message.channel.send(status)

    # white list command
    elif '+' in command.split(sep=' '):
        user = command.split(sep=' ')[1]
        logs.white_list(user)
        await message.channel.send(str(user) + ' white-listed for GPT3 API')

    # ban command
    elif '-' in command.split(sep=' '):
        user = command.split(sep=' ')[1]
        logs.session['ban_list'].append(str(user))
        logs.ban(user)
        await message.channel.send(str(user) + ' removed from white-list and ban from $ commands')

    else:
        await message.channel.send('options are [on] or [off], \nrecived invalid : ' + command)


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
