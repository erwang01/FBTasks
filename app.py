import requests
import os 
import sys
import json 
import config 
import re

from gensim.summarization import summarize
from urllib.parse import urlparse

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
						print("THE USER HAS GIVEN A URL.")
						USER_URL = message['text']
					if message.get('attachments'):
						print("THERE IS AN ATTACHMENT.")
						REAL_URL = message['attachments'][0]['URL']
						if REAL_URL:
							text = get_text(REAL_URL)
							output = ""
							for paragraph in text:
								output = output + summarize_text(paragraph)
							send_message(sender_id, output)

	return "Message Processed"


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
	return "Try again with a new URL"


def summarize_text(text):
	return summarize(text, ratio =0.4)







