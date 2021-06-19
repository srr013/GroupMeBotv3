import os
import json
from flask import Flask, request, session, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging
import importlib
import random

import settings
import services.config as config

import models.User as User
from models.GroupmeGroup import GroupmeGroup

import services.InboundMessage as InboundMessage

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#import after db is set
from models.Group import Group

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['GET','POST'])
def webhook():
	res = "No Message Posted"
	respStatus = 204
	if request.method == 'POST':
		payload = request.get_json()
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
		botIds = payload.get('botIds')
		groupName = payload.get('groupName', "default")
		if payload and groupId:
			g = db.session.query(Group).filter_by(groupId=groupId).first()
			if not g:
				group = Group(groupId, botIds, groupName)
				group.createGroupData()
				db.session.add(group)
				db.session.commit()
				return "Group created", 201
			else:
				g.botIds = botIds
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