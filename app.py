import os
import json
from flask import Flask, request, session, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging
import importlib
import random
import requests

import settings
import services.config as config


from services.GroupmeGroup import GroupmeGroup

import services.InboundMessage as InboundMessage

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#import after db is set
from models.Group import Group
from models.User import User
from models.Bot import Bot


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
			g.initializeGroupData()
			group = GroupmeGroup(g)
			res, respStatus = InboundMessage.parseMessage(request, group)
			db.session.commit()
		else:
			res = "Malformed message"
			respStatus = 404
	elif request.method == 'GET':
		res = "Fuck yourself!"
	return res, respStatus

@app.route('/healthCheck', methods=['GET'])
def healthCheck():
	return "Fuck yourself!", 200

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
				db.session.commit()
				return "Group created", 201
			else:
				g.botId = botId
				g.groupName = groupName
				g.messageTypes = payload.get('messageTypes', '{}')
				db.session.commit()
				return "Group updated", 201
		else:
			return "Group not found. Request missing data or not formatted", 400
	elif request.method == 'GET':
		groupList = db.session.query(Group).all()
		logging.warn(groupList)
		return json.dumps([g.deserialize() for g in groupList]), 200
	elif request.method == 'DELETE':
		if id:
			g = db.session.query(Group).filter_by(groupId=id).first()
			db.session.delete(g)
			db.session.commit()
			return "Group deleted", 200
		else:
			return "Group not found. Request missing data or not formatted", 400
	else:
		return "Method not allowed", 405

@app.route('/api/groupmegroups', methods=['GET'])
def manageGroupMeGroups(id = ''):
	if request.method == 'GET':
		url = "https://api.groupme.com/v3/groups?token="+config.GROUPME_ACCESS_TOKEN
		groups = requests.get(url)
		if groups:
			return groups.text, 200
		return "No groups found with provided access token", 400

@app.route('/api/bots', methods=['GET', 'POST'])
@app.route('/api/bots/<id>', methods=['GET', 'DELETE'])
def manageBots(id = ''):
	if request.method == 'POST':
		payload = request.get_json()
		groupId = str(payload.get('groupId'))
		g = db.session.query(Group).filter_by(groupId=groupId).first()
		if not g or groupId in config.TEST_GROUPS:
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
				db.session.commit()
				return "Bot created!", 201
			else:
				return f'Something happened: {res.content}', 400
		else:
			return f'Group {groupId} already has a bot assigned'
	elif request.method == 'DELETE' and id:
		b = db.session.query(Bot).filter_by(id=id).first()
		db.session.delete(b)
		db.session.commit()
		return "Bot deleted", 200
	elif request.method == 'GET':
		if id:
			botList = [db.session.query(Bot).filter_by(id=id).first()]
		else:
			botList = db.session.query(Bot).all()
		logging.warn(botList)
		return json.dumps([b.deserialize() for b in botList]), 200
	else:
		return "method not supported", 204