import os
import json
from flask import Flask, request, session, render_template
import logging

import settings
import models.Group as Group
import services.MessageAnalyzer as MessageAnalyzer
import services.Response as Response

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
		analyzer = MessageAnalyzer.MessageAnalyzer(payload)
		if analyzer.isGroupmePost:
			group_id = payload.get('group_id')
			group = Group.Group(group_id, groupme_access_token)
			response = Response.Response(group, analyzer)
			if analyzer.mentionAllMembers():
				response.mentionAll()
				response.send()
			elif analyzer.randomHouseSelector():
				response.randomHouseDraw()
				response.send()
			elif analyzer.help():
				response.help()
				response.send()
		return "Sent", 200
	else:
		return "OK"




# def get_message_loci(msg, names):
# 	loci = []
# 	for name in names:
# 		start = msg.find(name)
# 		if start:
# 			end = start + len(name)
# 			#logging.warning("Loci are: " + start +" " +end])
# 			loci.append([start, end])
# 	return loci
