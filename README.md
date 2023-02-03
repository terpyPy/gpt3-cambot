# gpt3-cambot

bot commands are:
```
all commands start with "$"

$GPT3 [option] : usage -- $GPT3 on
 on, turn gpt3 api commands on
 off, turn gpt3 api commands off
 +, add a discord user by full username(#0000 required) to whitelist
 -, ban a discord user by full username(#0000 required) and remove them from whitelist, and temp ban from all commands.

openAI api prompt commands are as follows:
 $QA, [prompt] : usage -- $QA your question here
 $py, [prompt] : usage -- $py python code or question.
 $re, [prompt] : usage -- $re reset the prompt cache for new prompt
 
none whitelist commands:
 $ping
 $fakehash [phrase to encrypt]
 $fakehash-d [phrase to decrypt]

console commands:
 *uses from program console only, not disc*
 - and +, add and remove a discord user by full username(#0000 required) to whitelist from console
 api on, turn api commands on
 api off, turn api commands off
 api -ld, prevent both openAPI and local commands from being used by anyone including admins+
 api -r remove the full locckdown on all commands
``

