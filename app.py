import requests
import os 
import sys
import json 
import config 

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Task

#Python libraries that we need to import for our bot
import random
from flask import Flask, request

app = Flask(__name__)

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
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                sender_id = message['sender']['id']
                if message['message'].get('text'):
                    handle_text_message(sender_id,message['message']['text'])
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(sender_id, response_sent_nontext)
    return "Message Processed"


def determine_if_task():
    #SOME CODE
    if (task):
        suggest_task()

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#Handles all user sent text messages
def handle_text_message(sender_id, text):
    #Check if they sent any command key words, if not run NLP algo
    method = commands.get(text, run_nlp)
    method(sender_id, text)

#Runs when the text sent is "completed task".
#Asks which task is completed and marks it done
def completed_task(sender_id, text):
    get_tasks(sender_id) #TODO: see if sender_id is sufficent, a single user may have multiple ids.
    send_message(sender_id, "Which task?")

#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

commands = {
    'completed task': completed_task
}

app.config['DEBUG'] = True
if __name__ == "__main__":
    app.run()

#Creates a new Task given these parameters
#Adds the task to the local database
def add_task(task_ID, task_title, task_detail, assigned_ID, deadline):
	task_to_be_added = Task(task_ID, task_title, task_detail, assigned_ID, deadline)
	db.session.add(task_to_be_added)
	db.session.commit()

#Deletes the specified Task object from the database
def delete_task(task): 
	db.session.delete(task)
	db.session.commit()

#Returns all tasks in database logged with 
#this User ID (string).
def query_task(user_id):
	tasks = User.query.filter_by(assigned_ID=user_id).all()
	return tasks




