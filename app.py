import os
import json
import datetime
from flask import Flask, request, session, render_template
import logging
import settings

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
groupme_access_token = os.environ.get('GM_ACCESS_TOKEN')
gm_bot_id = os.environ.get('GM_BOT_ID')


# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['GET','POST'])
def webhook():
    logging.warn("Request: "+request.get_json())
    if request.method == 'POST':
        message = request.get_json()
        group_id = message.get('response',{'group_id': None})['group_id']
        logging.warn("Group_id "+ str(group_id))
        msg = ''
        allOptions = ["@all","@All","@ALL", "@alL", "@aLl"]
        if group_id and any([x in msg for x in allOptions]):
            names, ids = get_user_names_and_ids(group_id)
            msg = create_message(names)
            send_message(msg, names, ids, gm_bot_id)
        return 200
    else:
        return "OK"

def create_message(users):
    msg = ""
    user_ids = []
    for user in users:
        msg += "@"+user[0]+", "
        user_ids.append(user[1])
    return msg

def get_user_names_and_ids(group_id):
    names = []
    ids = []
    url = "https://api.groupme.com/v3/groups/" + group_id + "?token="+groupme_access_token
    response = request.get(url)
    response = json.load(response)
    if isinstance(response.get("response"), dict):
        for member in response["response"]["members"]:
            names.append(member['nickname'])
            logging.warn("Name identified: "+ member['nickname'])
            ids.append(member["user_id"])
    return names, ids
    
def send_message(msg, names, user_ids, bot_id):
	# loop through users
		loci = get_message_loci(msg, names, user_ids) #need to insert '@username' in the text, identify start and end indices per-use
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

def get_message_loci(msg, names):
	loci = []
	for name in names:
		start = msg.index(name)
		if start:
			end = start + len(name)
		#logging.warning("Loci are: " + start +" " +end])
		loci.append([start, end])
	return loci
