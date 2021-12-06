import discord
from discord.client import Client
from chatBot import append_interaction_to_chat_log, ask
from tokenGen.passtool import tools
from logs import Logs
logs = Logs()

hasher = tools()


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        print(message.author, message.content)
        if message.content.startswith('$'):
            if not str(message.author) in logs.session['ban_list']:
                await self.on_command_anyone(message)
                if (str(message.author) in logs.auth_users):
                    await self.on_command_API(message)
                    await self.privileged_command(message)
                    print(logs.user_logs)
                else:
                    await message.channel.send(
                        'please ask terpy to be whitelisted these questions cost money')
            else:
                await message.channel.send(str(message.author) + ' is ban')

    async def on_command_anyone(self, message):
        if message.content.startswith('$he') or message.content.startswith('$?'):
            answer = ('usage:',
                      '\n$QA [your question],',
                      '\n$py [question about programing],',
                      '\n$reset: this resets prompt and memory',
                      '\n$fakehash: scramble a phrase',
                      '\n$fakehash-d: decrypt the phrase')

            print(message.author, 'on_command_whitelisted')
            await message.channel.send(' '.join(answer))

        elif message.content.startswith('$fakehash '):
            incoming_phrase = message.content[9:]
            h = hasher.getToken(incoming_phrase)
            print(message.author, 'on_command_whitelisted')
            await message.channel.send(h)
            # logs.user_logs[str(message.author)].append('on_command_whitelisted')

        elif message.content.startswith('$fakehash-d '):
            incoming_phrase = message.content[11:]
            h = hasher.decryption(incoming_phrase)
            print(message.author, 'on_command_whitelisted')
            await message.channel.send(h)
            # logs.user_logs[str(message.author)].append('on_command_whitelisted')
        elif message.content.startswith('$ping'):

            print(message.author, 'on_command_whitelisted')
            await message.channel.send(f"Pong! {round(client.latency * 1000)}ms")

    async def on_command_API(self, message):
        commands = ('$QA', '$py', '$re')
        if logs.session['API_access'] and len(logs.user_logs[str(message.author)]) < 6:
            if message.content.startswith(commands[0]):
                answer = self.get_awnser(message, 'QA')
                await message.channel.send(answer)
                print(message.author, 'on_command_API')
                logs.user_logs[str(message.author)].append('on_command_API')

            elif message.content.startswith(commands[1]):
                answer = self.get_awnser(message, 'py')
                await message.channel.send(answer)
                print(message.author, 'on_command_API')
                logs.user_logs[str(message.author)].append('on_command_API')

            elif message.content.startswith(commands[2]):
                logs.DB_update()
                logs.session['chat_log'] = None
                await message.channel.send("conversation and respones cache cleared.")
                print(message.author, 'on_command_API')

        elif not logs.session['API_access'] and str(message.content)[:3] in commands:
            await message.channel.send('api access is unavailable contact ' + logs.admin)

    async def privileged_command(self, message):
        is_command = message.content.startswith('$GPT3 ')
        if (str(message.author) == logs.admin):

            if is_command:
                print(message.author, 'privileged_command')
                command = message.content[6:]
                print(command)
                await self.admin_options(command, message)

        if not (str(message.author) == logs.admin) and is_command:
            logs.session['ban_list'].append(str(message.author))
            logs.ban(str(message.author))

            await message.channel.send(
                '@' + str(message.author) + ' you\'re attempt to use privilege commands has notified ' + logs.admin + '\nyour privileges and whitelist are revoked , and the attempt was logged')

    async def admin_options(self, command, message):

        if command == 'on':
            logs.session['API_access'] = True
            await message.channel.send('GPT3 api access is online')

        elif command == 'off':
            logs.session['API_access'] = False
            await message.channel.send('GPT3 api access is offline')

        elif '+' in command.split(sep=' '):
            user = command.split(sep=' ')[1]
            logs.white_list(user)
            await message.channel.send(str(user) + ' white-listed for GPT3 API')

        elif '-' in command.split(sep=' '):
            user = command.split(sep=' ')[1]
            logs.session['ban_list'].append(str(user))
            logs.ban(user)
            await message.channel.send(str(user) + ' removed from white-list and ban from $ commands')

        else:
            await message.channel.send('options are [on] or [off], \nrecived invalid : ' + command)

    def get_awnser(self, message, command='QA'):
        # parse input to exclude $ask
        incoming_msg = message.content[4:]
        # get chat log and then,
        chat_log = logs.session['chat_log']
        # ask question with incoming message and chat log
        answer = ask(incoming_msg, chat_log)
        # add both entry's to the chatlog
        logs.session['chat_log'] = append_interaction_to_chat_log(incoming_msg,
                                                                  answer,
                                                                  chat_log,
                                                                  command
                                                                  )
        print(logs.session['chat_log'])
        return answer


client = MyClient()
client.run(logs.session['disc_auth'])
