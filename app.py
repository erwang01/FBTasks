import requests
import os 
import sys
import json 
import config 

from gensim.summarization import summarize

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Task
from bs4 import BeautifulSoup

#Python libraries that we need to import for our bot
from flask import Flask, request


app = Flask(__name__)
ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                sender_id = message['sender']['id']
                if message.get('message'):
                    if message['message'].get('text'):
                        handle_message(sender_id, message['message']['text'] )

                if message.get('attachment'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    if message['message'].get('attachement'):
                        handle_message(sender_id, message['message']['attachment']['payload']['url'])

    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def handle_message(sender_id, message):
    send_message(sender_id, message)
#sends message to user
def send_message(recipient_id, message):
    endpointURL = "https://graph.facebook.com/v2.6/me/messages?access_token="+ACCESS_TOKEN
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message
        }
    }
    header = {"Content-Type": "application/json"}
    fb_response = requests.post(endpointURL, data=json.dumps(payload), headers=header)
    return fb_response

app.config['DEBUG'] = True
if __name__ == "__main__":
    app.run()

def get_text(url):
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = []
        for paragraph in paragraphs:
            snippet = paragraph.get_text()
            if len(snippet) > 250:
                print(snippet)
                text.append(paragraph.get_text())
    return text



def summarize_text(text):
    return summarize(text, ratio =0.2)







