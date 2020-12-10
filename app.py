import os
import json
import datetime
from flask import Flask, request, session, render_template
import logging

from requests.models import encode_multipart_formdata
import settings
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
groupme_access_token = os.environ.get('GM_ACCESS_TOKEN')

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['GET','POST'])
def webhook():
	if request.method == 'POST':
		logging.warn("Request: "+json.dumps(request.get_json()))
		payload = request.get_json()
		if payload['sender_type'] != "bot":
			group_id = payload.get('group_id')
			logging.warn("Group_id "+ str(group_id))
			msg = ''
			allOptions = ["@all","@All","@ALL", "@alL", "@aLl"]
			msg_text = payload.get("text")
			if group_id and any([x in msg_text for x in allOptions]):
				start_text, end_text = get_surrounding_text(msg_text)
				gm_bot_id = os.environ.get('GM_BOT_ID_TEST')
				if group_id == '60197068':
					gm_bot_id = os.environ.get('GM_BOT_ID')
				names, ids = get_user_names_and_ids(group_id)
				mentions = create_mention_text(names)
				msg = create_message(mentions, start_text, end_text)
				send_message(msg, names, ids, gm_bot_id)
		return "Sent", 200
	else:
		return "OK"

def create_message(mentions, start_text, end_text):
	return start_text + mentions + end_text

def get_surrounding_text(msg_text):
	l = msg_text.lower()
	start_index = l.find("@all")
	start_text = ""
	if start_index > 0:
		start_text = msg_text[0:start_index]
	end_index = start_index + 4
	end_text = msg_text[end_index+1:len(msg_text)]
	logging.warn("start text: "+start_text)
	logging.warn("end text: "+end_text)

	return start_text, end_text

def create_mention_text(names):
	msg = ""
	for name in names:
		msg += "@"+name+", "
	msg = msg[0:-2]
	return msg

def get_user_names_and_ids(group_id):
	names = []
	ids = []
	url = "https://api.groupme.com/v3/groups/" + group_id + "?token="+groupme_access_token
	response = requests.get(url)
	logging.warn("Response: "+response.text)
	response = json.loads(response.text)
	if response.get("response"):
		for member in response["response"]["members"]:
			names.append(member['nickname'])
			logging.warn("Name identified: "+ member['nickname'])
			ids.append(member["user_id"])
	return names, ids
	
def send_message(msg, names, user_ids, bot_id):
	loci = get_message_loci(msg, names)
	if user_ids and loci:
		d = {'bot_id': bot_id,
				'text': msg,
				'attachments': [
					{"type": "mentions",
					"loci": loci,
					"user_ids": user_ids}
				]
			}
		url = "https://api.groupme.com/v3/bots/post"
		resp = requests.post(url, json=d)
		if resp.status_code == 202:
			logging.warn("Message Posted")
		else:
			logging.warn("Message failed to post: "+ str(resp.status_code))
	else:
		logging.warn("User IDs or loci not set")

def get_message_loci(msg, names):
	loci = []
	for name in names:
		start = msg.find(name)
		if start:
			end = start + len(name)
			#logging.warning("Loci are: " + start +" " +end])
			loci.append([start, end])
	return loci
