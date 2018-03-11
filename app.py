import requests
import random
import os 
import sys
import json 
import config 
import re

from gensim.summarization import summarize

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
					print("THERE IS A SENDER.")
					sender_id = messaging['sender']['id']
					if messaging.get('message'):
						print("AND THERE IS A MESSAGE.")
						message = messaging['message']
						if message.get('text'):
							print("THE USER HAS GIVEN US TEXT.")
							USER_URL = message['text']
						if message.get('attachments'):
							print("THERE IS AN ATTACHMENT.")
							attachment = message['attachments'][0]
							if attachment.get('url'):
								print("THERE IS A URL.")
								REAL_URL = attachment['url']
								if REAL_URL:
									text = summarize_text(get_text(REAL_URL))
									sentences = text.split(".")
									print("TEXT HAS BEEN ACQUIRED.")
									for sent in sentences:
										output = ""
										print(sent + "\n")
										if not sent.find(".")==-1:
											output=sent + " "
										else:
											output=sent + ". "
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
	return "Message Processed"

def random_greet():
	greetings = ["Hi! I'm here to help. Send me articles, stories, anything you want summarized.",
				'Hello! I summarize articles into their key points to help you learn and save you time.',
				'Hey!', 'Hello to you too.', 'Hi. Anything you need summarized?', 'Hello!']
	index = random.randint(0, len(greetings)-1)
	return greetings[index]

def random_your_welcome():
	welcome = ['No problem!', "I'm always happy to help!", 'Sure thing!', "You're very welcome.", "Anytime!"
				'Glad to be of use!', 'Of course!', "You're welcome!"]
	index = random.randint(0, len(welcome)-1)
	return welcome[index]

def verify_fb_token(token_sent):
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return 'Nothing to see here.'


url_regex_full = re.compile(
		r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)

url_regex_half = re.compile(
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)



"""
def handle_message(sender_id, message):
	print(message)
	tokens = message.split(" ")
	urls = []
	for token in tokens:
		print("The token is this: " + token)
		result = url_regex_full.search(token)
		if result:
			urls.append(token)
			print("Token immediately successful.")
		else:
			result = url_regex_half.search(token)
			if result:
				o = urlparse(token)
				replaced = o
				if o.scheme!='http' and o.scheme!='https':
				   replaced = o._replace(scheme='http')
				   print('This url was altered to ' + replaced.geturl())
				   print(o.geturl())
				#if not o.netloc: 
					#pass
				try:
					#requests.get(replaced.geturl(), timeout = 1.0)
					history = requests.get(replaced.geturl())
					print(history)
					#urls.append(replaced.geturl())
				except:
					print('Exception.')
					pass
	if len(urls)==0:
		send_message(sender_id, "Sorry, I couldn't make a link out of this.")
		return 
	else:
		send_message(sender_id, urls[0])
		send_message(sender_id, get_text(urls[0])[1])
"""

"""
#sends message to user
def send_message(recipient_id, message):
	print("TRYING TO SEND A MESSAGE");
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
"""
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

app.config['DEBUG'] = True
if __name__ == "__main__":
	app.run()


def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		return False
	elif re.match('<!--.*-->', str(element.encode('utf-8'))):
		return False
	return True

def get_text(url):
	page = requests.get(url)
	url_container = page.headers['Refresh']
	index = url_container.find('http')
	end_url = ""
	if index!=-1:
		end_url = url_container[index:]
	print("THE FINAL URL:" + end_url)
	real_page = requests.get(end_url)
	if page.status_code == 200:
		soup = BeautifulSoup(real_page.content, 'html.parser')
		data = soup.findAll(text=True)
		result = filter(visible, data)
		text = ""
		for res in result:
			text+=res
		return text
	return "Try again with a new URL"


def summarize_text(text):
	return summarize(text, ratio=.020)









