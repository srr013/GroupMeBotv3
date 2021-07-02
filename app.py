import os
import json
from flask import Flask, request, session, render_template, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging
import requests

import settings
import services.config as config


from services.GroupmeGroup import GroupmeGroup
import services.InboundMessage as InboundMessage
from services.Response import Response as MessageResponse



app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#import after db is set
from models.Group import Group
# from models.User import User
from models.Bot import Bot
import models.OutboundMessage as OutboundMessage


# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['GET','POST'])
@app.route('/<groupId>', methods=['GET','POST'])
def webhook(groupId = ''):
	res = "No Message Posted"
	respStatus = 204
	if request.method == 'POST':
		payload = request.get_json()
		if not groupId:
			groupId = payload.get('group_id')
		if groupId:
			g = db.session.query(Group).filter_by(groupId=groupId).first()
			if g:
				g.initializeGroupData()
				group = GroupmeGroup(g)
				response = MessageResponse(group, payload)

				#set the messageObject to send the message from that object
				#check for written triggers
				response.messageObject = InboundMessage.parseMessageContent(payload, group, response)
				#check for random content
				if not response.messageObject:
					if group.readyForMessage():
						response.messageObject = response.getTriggeredResponse(group)
				
				#send the queued message
				if response.messageObject:
					response.responseText = response.messageObject.constructResponseText(payload, response)
					response.messageObject.updateGroupData(g)
					outboundMessage = OutboundMessage.OutboundMessage(response)
					db.session.add(outboundMessage)
					res, respStatus = response.send()
				db.session.commit()
			else:
				res = "Group not found"
				respStatus = 404
		else:
			res = "Malformed message"
			respStatus = 404
	return Response(res, status=respStatus, content_type='application/json')

@app.route('/healthCheck', methods=['GET'])
def healthCheck():
	res = "Fuck yourself!"
	respStatus = 200
	return Response(res, status=respStatus, content_type='application/json')

@app.route('/api/authorize', methods=['POST'])
def validateToken():
	import services.jwt as jwtService

	body = request.get_json()
	# fn = body.get('firstName')
	# ln = body.get('lastName')
	email = body.get('email')
	if email:
		user = User.User(body)
		logging.warn(user.email)
	return "validated", 200

@app.route('/api/groups', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/groups/<id>', methods=['GET', 'PUT', 'DELETE'])
def manageGroups(id = ''):
	if request.method == 'PUT': #upsert the group
		#TODO secure this endpoint
		payload = request.get_json()
		groupId = payload.get('groupId')
		botId = payload.get('botId')
		groupName = payload.get('groupName', "default")
		if payload and groupId:
			g = db.session.query(Group).filter_by(groupId=groupId).first()
			if not g:
				group = Group(groupId, botId, groupName)
				group.createGroupData()
				db.session.add(group)
				res = "Group created"
				respStatus = 201
			else:
				if botId:
					g.botId = botId
				if groupName:
					g.groupName = groupName
				if payload.get('messageTypes'):
					g.messageTypes = payload.get('messageTypes')
				res = "Group updated"
				respStatus = 201
		else:
			res = "Group not found. Request missing data or not formatted"
			respStatus = 400
	elif request.method == 'GET':
		groupList = db.session.query(Group).all()
		res = json.dumps({"groups":[g.deserialize() for g in groupList]})
		respStatus = 200
	elif request.method == 'DELETE':
		if id:
			g = db.session.query(Group).filter_by(groupId=id).first()
			db.session.delete(g)
			res = "Group deleted"
			respStatus = 200
		else:
			res = "Group not found. Request missing data or not formatted"
			respStatus = 400
	else:
		res = "Method not allowed"
		respStatus = 405
	db.session.commit()
	return Response(res, status=respStatus, content_type='application/json')

@app.route('/api/groupmegroups', methods=['GET'])
def manageGroupMeGroups(id = ''):
	if request.method == 'GET':
		url = "https://api.groupme.com/v3/groups?token="+config.GROUPME_ACCESS_TOKEN
		groups = requests.get(url)
		if groups:
			res = groups.text
			respStatus = 200
		else:
			res = "No groups found with provided access token"
			respStatus = 400
	else:
		res = "Method not supported"
		respStatus = 404
	return Response(res, status=respStatus, content_type='application/json')

@app.route('/api/bots', methods=['GET', 'POST'])
@app.route('/api/bots/<id>', methods=['GET', 'DELETE', 'POST'])
def manageBots(id = ''):
	if request.method == 'POST':
		payload = request.get_json()
		groupId = str(payload.get('groupId'))
		g = db.session.query(Group).filter_by(groupId=groupId).first()
		if g and payload.get("id"):
			bot = Bot(payload["id"], payload["botName"], payload["botCallbackUrl"], payload["avatarUrl"])
			g.botId = payload["id"]
			db.session.add(bot)
			res = "Bot created in DB and group updated! No GroupMe Action taken."
			respStatus  = 201
		elif not g or groupId in config.TEST_GROUPS:
			botName = payload.get('botName')
			botCallbackUrl = payload.get('botCallbackUrl')
			avatarUrl = payload.get('avatarUrl')
			groupName = payload.get('groupName')
			url = "https://api.groupme.com/v3/bots?token="+config.GROUPME_ACCESS_TOKEN
			body = {
				"bot": {
					"name": botName,
					"group_id": groupId,
				}
			}
			if botCallbackUrl:
				body['bot']['callback_url'] = botCallbackUrl
			if avatarUrl:
				body['bot']['avatar_url'] = avatarUrl
			headers = {
				"Content-Type": "application/json"
			}
			res = requests.post(url, data=json.dumps(body), headers=headers)
			if res.status_code == 201:
				botData = res.json()
				botData = botData['response']['bot']
				bot = Bot(botData['bot_id'], botData['name'], botData['callback_url'], botData['avatar_url'])
				group = Group(groupId, bot.id, groupName)
				group.createGroupData()
				db.session.add(bot)
				db.session.add(group)
				res = "Bot created!"
				respStatus  = 201
			else:
				res = f'Something happened: {res.content}'
				respStatus = 400
		else:
			res = f'Group {groupId} already has a bot assigned. Use PUT to update'
			respStatus = 200
	elif request.method == 'DELETE' and id:
		b = db.session.query(Bot).filter_by(id=id).first()
		db.session.delete(b)
		res = "Bot deleted"
		respStatus = 200
	elif request.method == 'GET':
		if id:
			botList = [db.session.query(Bot).filter_by(id=id).first()]
		else:
			botList = db.session.query(Bot).all()
		logging.warn(botList)
		res = json.dumps({"bots": [b.deserialize() for b in botList]})
		respStatus = 200
	else:
		res = "Method not supported"
		respStatus = 204
	db.session.commit()
	return Response(res, status=respStatus, content_type='application/json')