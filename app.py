from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from chatBot import ask, append_interaction_to_chat_log
from chat_tokens import tokens

app = Flask(__name__)
chat_sessions = tokens()
session_token = chat_sessions.sessions['0']
# if for some reason your conversation with Jabe gets weird, change the secret key
app.config['SECRET_KEY'] = session_token # session key variable
@app.route('/cambot', methods=['POST'])
def cambot():
 incoming_msg = request.values['Body']
 if '!reset' in incoming_msg:
    app.config['SECRET_KEY'] = chat_sessions.sessions['1']
 chat_log = session.get('chat_log')
 answer = ask(incoming_msg, chat_log)
 session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,
 chat_log)
 msg = MessagingResponse()
 msg.message(answer)
 return str(msg)

if __name__ == '__main__':
 app.run(debug=True)