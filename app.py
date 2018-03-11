import requests
import os 
import sys
import json 
import config 


from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Task
from bs4 import BeautifulSoup

import gensim 

#Python libraries that we need to import for our bot
from flask import Flask, request

app = Flask(__name__)
ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)


def create_model(session, ckpt): 
    dtype = tf.float32
    model = bigru_model.BiGRUModel(
        FLAGS.doc_vocab_size,
        FLAGS.sum_vocab_size,
        _buckets,
        FLAGS.size,
        FLAGS.num_layers,
        FLAGS.embsize,
        FLAGS.max_gradient,
        FLAGS.batch_size,
        FLAGS.learning_rate,
        forward_only=forward_only,
        dtype=dtype)
    if ckpt and tf.train.checkpoint_exists(ckpt):
        logging.info("Reading model parameters from %s" % ckpt)
        model.saver.restore(session, ckpt)
    return model

def eval():
    logging.info("Preparing summarization data.")
        docid, sumid, doc_dict, sum_dict = \
        data_util.load_data(
            FLAGS.data_dir + "/train.article.txt",
            FLAGS.data_dir + "/train.title.txt",
            FLAGS.data_dir + "/doc_dict.txt",
            FLAGS.data_dir + "/sum_dict.txt",
            FLAGS.doc_vocab_size, FLAGS.sum_vocab_size)

        val_docid, val_sumid = \
            data_util.load_valid_data(
                FLAGS.data_dir + "/valid.article.filter.txt",
                FLAGS.data_dir + "/valid.title.filter.txt",
                doc_dict, sum_dict)

        with tf.Session() as sess:

        logging.info("Creating %d layers of %d units." %
                     (FLAGS.num_layers, FLAGS.size))
        train_writer = tf.summary.FileWriter(FLAGS.tfboard, sess.graph)
        model = create_model(sess, False)

        # Read data into buckets and compute their sizes.
        logging.info("Create buckets.")
        dev_set = create_bucket(val_docid, val_sumid)
        train_set = create_bucket(docid, sumid)

        train_bucket_sizes = [len(train_set[b]) for b in range(len(_buckets))]
        train_total_size = float(sum(train_bucket_sizes))
        train_buckets_scale = [
            sum(train_bucket_sizes[:i + 1]) / train_total_size
            for i in range(len(train_bucket_sizes))]

        for (s_size, t_size), nsample in zip(_buckets, train_bucket_sizes):
            logging.info("Train set bucket ({}, {}) has {} samples.".format(
                s_size, t_size, nsample))


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
                    handle_message(sender_id, message['message']['text'] )

    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def handle_message(sender_id, message):
    user = db.session.query(User).get(sender_id)
    if user == None:
        if message=='Start':
            send_message(sender_id, 'Initial Contact made. Open me as an extension!')
        else:
            send_message(sender_id, 'Hey, I operate as a chat extension. Find me in your chats!')
        db.session.add(User(sender_id, user_name, user_fullname))
    else:
        send_message(sender_id, "You currently have the following tasks to complete")
        for task in get_tasks(sender_id):
            send_message(sender_id, task)
    db.session.commit()
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
        print(soup.prettify())
        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            print(paragraph)
            if len(paragraph) < 1000:
                paragraphs.remove(paragraph)
    return paragraphs










