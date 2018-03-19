import requests
import random
import os 
import sys
import json 
import config 
import re

from gensim.summarization import summarize
from readability import Document

from flask import Flask, request
from bs4 import BeautifulSoup

app = Flask(__name__)
ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

print("********************************")
print("app.py starting")



#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
	if request.method == 'GET':
		token_sent = request.args.get("hub.verify_token")
		return verify_fb_token(token_sent)
	#if the request was not get, it must be POST and we can just proceed with sending a message back to user
	else:
		# get whatever message a user sent the bot
		output = request.get_json()
		print(output)
		for event in output['entry']:
			if event.get('messaging'):
				messaging = event.get('messaging')[0]
				if messaging.get('sender'):
					sender_id = messaging['sender']['id']
					if messaging.get('message'):
						message = messaging['message']
						if message.get('text'):
							USER_URL = message['text']
						if message.get('attachments'):
							attachment = message['attachments'][0]
							if attachment.get('url'):
								REAL_URL = attachment['url']
								if REAL_URL:
									text = get_text(REAL_URL)
									print("This is the text: " + text)
									summary = summarize_text(text)
									print("This is the summary:" + summary)
									sentences = summary.split(".")
									print("TEXT HAS BEEN ACQUIRED.")
									print("the sentences are:" + str(sentences))
									for sent in sentences:
										output = ""
										if sent:
											print(sent + "\n")
											if not sent.find(".")==-1:
												output=sent+" "
											else:
												output=sent+". "
											send_message(sender_id, output)
						if message.get('nlp'):
							nlp = message['nlp']
							if nlp.get('entities'):
								entities = nlp['entities']
								if entities.get('thanks'):
									if entities['thanks'][0]['confidence'] > 0.5:
										send_message(sender_id, random_your_welcome())
								if entities.get('greetings'):
									if entities['greetings'][0]['confidence'] > 0.5:
										send_message(sender_id, random_greet())
					elif messaging.get("postback"):
						received_postback(messaging)
	return "Message Processed"

def random_greet():
	greetings = ["Hi! I'm here to help. Send me articles, stories, anything you want summarized.",
				'Hello! I summarize articles into their key points to help you learn and save you time.',
				'Hey!', 'Hello to you too.', 'Hi. Anything you need summarized?', 'Hello!']
	index = random.randint(0, len(greetings)-1)
	return greetings[index]

def random_your_welcome():
	welcome = ['No problem!', "I'm always happy to help!", 'Sure thing!', "You're very welcome.", "Anytime!",
				'Glad to be of use!', 'Of course!', "You're welcome!"]
	index = random.randint(0, len(welcome)-1)
	return welcome[index]

def verify_fb_token(token_sent):
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return 'Nothing to see here.'

def send_message(recipient_id, message):
	print("TRYING TO SEND A MESSAGE")
	params = { "access_token": ACCESS_TOKEN }
	headers = {	"Content-Type": "application/json" }
	data = json.dumps({
		"recipient": {
			"id": recipient_id
		},
		"message": {
			"text": message
		}
	})
	r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
	print(r)

app.config['DEBUG'] = True
if __name__ == "__main__":
	app.run()


def get_text(url):
	page = requests.get(url)
	url_container = page.headers['Refresh']
	index = url_container.find('http')
	end_url = ""
	if index!=-1:
		end_url = url_container[index:]
	print("THE FINAL URL:" + end_url)
	real_page = requests.get(end_url)
	if real_page.status_code == 200:
		doc = Document(real_page.text)
		summary_unclean = doc.summary(True)
		soup = BeautifulSoup(summary_unclean, "lxml")
		text = soup.get_text().split("\n")
		print("Result of soup.get_text().split()" + str(text))
		content = ""
		for t in text:
			if len(t) > 100:
				print('This is being added. ADD ADD')
				content+=t
			print("Here's a chunk of text:" + t + "\n")
		print("Here's the content we are returning from get_text:" + content)
		return content
	return "Try again with a new URL"


def summarize_text(text):
	return summarize(text, ratio=.05)

def received_postback(event):
	sender_id = event["senter"]["id"] #ID of sender
	recipient_id = event["recipient"]["id"] #ID of QuickRead

	payload = event["postback"]["payload"]

	print("received postback from {recipient} with payload {payload}".format(recipient=recipient_id, payload=payload))

	if payload == 'Get Started':
		#Get Started button was pressed
		random_greet()
	else:
		send_message(sender_id, "Postback was called with payload {payload}".format(payload=payload))