import threading
import discord
from discord.client import Client
from chatBot import append_interaction_to_chat_log, ask
from tokenGen.passtool import tools
import logsConsole
import time


startTime = time.time()
hours = 0
hasher = tools()
client = discord.Client()
cmd = logsConsole.console()


@client.event
async def on_ready():
    # let yourclient know when the bot is ready to be propmeted on startup
    print('Logged on as {0}!'.format(client.user))

@client.event
async def on_message(message):
    # prevent the bot from using or echoing commands it sends
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        # check the temp ban list stored in memory
        author = str(message.author)

        # if the user is not in the temp ban list continue
        if not author in cmd.session['ban_list']:
            # everyone privileged commands
            respons = on_command_anyone(message, author)

            # if not ban and the command is whitelist scope
            # check if user is whitelisted
            if not respons:

                respons = on_command_API(message, author)

            elif (author in cmd.auth_users):
                    respons = privileged_command(message, author)

        else:
            respons = author + ' is ban'

        await message.channel.send(respons)

def on_command_anyone(message, author):
    returnMsg = None
    if message.content.startswith('$he') or message.content.startswith('$?'):
        answer = ('usage:',
                  '\n$QA [your question],',
                  '\n$py [question about programing],',
                  '\n$reset: this resets prompt and memory',
                  '\n$fakehash: scramble a phrase',
                  '\n$fakehash-d: decrypt the phrase')

        return ' '.join(answer)

    elif message.content.startswith('$fakehash '):
        incoming_phrase = message.content[9:]
        returnMsg = hasher.getToken(incoming_phrase)

    elif message.content.startswith('$fakehash-d '):
        incoming_phrase = message.content[11:]
        returnMsg = hasher.decryption(incoming_phrase)

    elif message.content.startswith('$ping'):
        returnMsg = (f"Pong! {round(client.latency * 1000)}ms")

    elif message.content.startswith('$uptime'):
        returnMsg = str(cmd.uptime(startTime, hours))

    if returnMsg != None:
        print('\n', author, ' On_command_anyone')

    return returnMsg

def on_command_API(message, author):
    responded = None
    # TODO: Refactor this with helper functions to support checking msg content, and only await one awnser back.
    # OpenAI bot commands, only whitelisted users can propmet the bot and reset the propmet history
    commands = ('$QA', '$py', '$re', '$ts')
    if cmd.session['API_access'] and len(cmd.user_logs[author]) < 6:

        if message.content.startswith(commands[0]):
            responded = get_awnser(message, 'QA')

            cmd.user_logs[author].append('on_command_API')

        elif message.content.startswith(commands[1]):
            responded = get_awnser(message, 'py')

            cmd.user_logs[author].append('on_command_API')

        elif message.content.startswith(commands[3]):
            responded = get_awnser(message, 'test')

            cmd.user_logs[author].append('on_command_API')

        elif message.content.startswith(commands[2]):
            cmd.DB_update()
            cmd.session['chat_log'] = None
            responded = "conversation and respones cache cleared."
            
        elif responded != None:
            print('\n', author, 'API_command')
        # return message
        return responded

    elif not cmd.session['API_access'] and str(message.content)[:3] in commands:
        return ('api access is unavailable contact ' + cmd.admin)

def privileged_command(message, author):
    # admin scope check & auto ban for attempted use,
    #
    # check the message for just the command
    is_command = (message.content.startswith('$GPT3 ')
                  or message.content.startswith('$cmd -'))
    command = message.content[6:]

    if (author == cmd.admin):

        if is_command:
            print('\n', author, 'Admin_command')
            # parse the message for just the command
            msg = admin_options(command, message)
            return msg

    if not (author == cmd.admin) and is_command:
        # auto ban users that attempt to use admin scope commands, also removes from whitelist if present.
        cmd.session['ban_list'].append(author)
        cmd.ban(author)
        return ('@' + author + ' you\'re attempt to use privilege commands has notified '
                + cmd.admin + '\nyour privileges and whitelist are revoked , and the attempt was logged')

def admin_options(command, message):
    # admin privilege commands
    #
    # GPT 3 api access control
    table = ('on', 'off')
    if command in table:
        status = cmd.api_access(command)
        return status

    elif command == 'h':
        cmdResponse = cmd.hook(message)
        return cmdResponse

    # white list command
    elif '+' in command.split(sep=' '):
        user = command.split(sep=' ')[1]
        cmd.white_list(user)
        return str(user) + ' white-listed for GPT3 API'

    # ban command
    elif '-' in command.split(sep=' '):
        user = command.split(sep=' ')[1]
        cmd.session['ban_list'].append(str(user))
        cmd.ban(user)
        return str(user) + ' removed from white-list and ban from $ commands'

    else:
        return 'options are [on] or [off], \nrecived invalid : ' + command


def get_awnser(message, command='QA'):
    # parse input to exclude $ask
    incoming_msg = message.content[4:]
    # get chat log and then,
    chat_log = cmd.session['chat_log']
    # ask question with incoming message and chat log
    answer = ask(incoming_msg, chat_log)
    # add both entry's to the chatlog
    cmd.session['chat_log'] = append_interaction_to_chat_log(incoming_msg,
                                                             answer,
                                                             chat_log,
                                                             command
                                                             )
    # print(cmd.session['chat_log'])
    return answer


if __name__ == '__main__':
    threading.Thread(target=cmd.main,
                     args=(), daemon=True).start()
    client.run(cmd.session['disc_auth'])
