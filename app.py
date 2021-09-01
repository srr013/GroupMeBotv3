import os
import json
from flask import Flask, request, session, render_template, Response
from flask.helpers import send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging
import requests
from werkzeug.utils import secure_filename

import settings
import services.config as config


from services.GroupmeGroup import GroupmeGroup

from services.Response import Response as MessageResponse
import services.aws as AWS

import models.MessageTypes.SendMessageFromAPI as SendMessageFromAPI

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
db = SQLAlchemy(app)

#import after db is set
from models.Group import Group
# from models.User import User
from models.Bot import Bot
import models.OutboundMessage as OutboundMessage
import models.InboundMessage as InboundMessage


# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['GET','POST'])
@app.route('/<groupId>', methods=['GET','POST'])
def webhook(groupId = ''):

	if request.method == 'POST':
		res = "No Message Posted"
		respStatus = 204
		payload = request.get_json()
		inboundMessage = {}
		if payload.get("group_id"):
			if groupId != payload.get("group_id"):
				logging.info(f"Message group ID and endpoint don't match. Message contents has groupID:{inboundMessage.grouId} while endpoint is {groupId}")
				inboundMessage.groupId = groupId
			inboundMessage = InboundMessage.InboundMessage(payload)
			# db.session.add(inboundMessage)
			if inboundMessage:
				g = db.session.query(Group).filter_by(groupId=inboundMessage.groupId).first()
				if g:
					g.initializeGroupData()
					groupMeGroup = GroupmeGroup(g)
					if not inboundMessage.isBotOrSystemMessage(payload):
						groupMeGroup.incrementCounter()
					response = MessageResponse(groupMeGroup, payload)
					bot = db.session.query(Bot).filter_by(id=g.botId).first()
					groupMeGroup.bot = bot
					#set the messageObject to send the message from that object
					#check for written triggers
					response.messageObject = inboundMessage.parseMessageContent(payload, groupMeGroup, response, bot)
					#check for random content
					if not response.messageObject:
						if groupMeGroup.readyForMessage():
							response.messageObject = response.getTriggeredResponse(groupMeGroup)
					
					#send the queued message
					if response.messageObject:
						response.responseText = response.messageObject.constructResponseText(payload, response)
						response.messageObject.updateGroupData()
						outboundMessage = OutboundMessage.OutboundMessage(response)
						inboundMessage.outboundMessage = outboundMessage
						db.session.add(outboundMessage)
						res, respStatus = response.send()
				else:
					res = "Group not found"
					respStatus = 404
			else:
				res = "Malformed message"
				respStatus = 404
		db.session.commit()
		return Response(res, status=respStatus, content_type='application/json')

	if request.method == 'GET':
		images, status = AWS.getBucketContents(config.BUCKET_NAME)
		images = json.loads(images)
		return render_template('index.html', imageList = images)

@app.route('/api/sendMessage/<groupId>', methods=['POST'])
def sendMessage(groupId = ''):
	res = "No groupId provided"
	respStatus = 204
	payload = request.get_json()
	if groupId:
		if groupId:
			g = db.session.query(Group).filter_by(groupId=groupId).first()
			if g:
				g.initializeGroupData()
				groupMeGroup = GroupmeGroup(g)
				response = MessageResponse(groupMeGroup, payload)
				bot = db.session.query(Bot).filter_by(id=g.botId).first()
				groupMeGroup.bot = bot
				response.messageObject = SendMessageFromAPI.SendMessageFromAPI(groupMeGroup)
				if payload.get('isImage'):
					bucket = AWS.getBucket('insultbot-memes')
					fileObjs = AWS.getFileObjsFromBucket(bucket, payload.get("imageName"))
					if fileObjs:
						response.messageObject.responseType = 'image'
						response.responseText = AWS.downloadFileFromBucket(bucket, fileObjs[0])
					else:
						response.responseText = None
				else:
					if payload.get('message'):
						response.messageObject.responseType = 'text'
						response.responseText = payload.get('message')
					else:
						response.responseText = None
				if response.responseText:
					outboundMessage = OutboundMessage.OutboundMessage(response)
					db.session.add(outboundMessage)
					res, respStatus = response.send()
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
				group = Group(groupId, botId, groupName, payload=payload)
				group.createGroupData()
				db.session.add(group)
				res = "Group created"
				respStatus = 201
			else:
				if botId:
					g.botId = botId
				if groupName != 'default':
					g.groupName = groupName
				if payload.get('messageTypes'):
					g.messageTypes = payload.get('messageTypes')
				if 'messagingServiceStatus' in payload.keys():
					g.messagingServiceStatus = payload.get('messagingServiceStatus')
				if 'active' in payload.keys():
					g.active = payload.get('active')
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
		if payload.get("id"):
			bot = db.session.query(Bot).filter_by(id=id).first()
			if not bot:
				bot = Bot(payload["id"], payload["botName"], payload["botCallbackUrl"], payload["avatarUrl"])
			if g:
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

@app.route('/api/buckets', methods=['GET', 'POST', 'DELETE', 'PUT'])
@app.route('/api/buckets/<bucketName>', methods=['GET', 'DELETE', 'PUT'])
def manageBuckets(bucketName = ''):
	if not bucketName:
		bucketName = config.BUCKET_NAME
	filename = ''
	if request.args.get("filename"):
		filename = request.args.get("filename")

	if request.method == 'GET':
		res, status = AWS.getBucketContents(bucketName)
		return Response(json.dumps({"text": res}), status=status, content_type='application/json')
	elif request.method == 'POST':
		res = 'No file provided'
		respStatus = 404
		if filename or 'file' in request.files:
			if filename:
				res, status =  AWS.putFileInBucket(filename, bucketName)
			else:
				file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
				if file.filename:
					if AWS.allowed_file(file.filename):
						filename = secure_filename(file.filename)
						file.save(os.path.join(config.UPLOAD_FOLDER, filename))
					else:
						res = f"File extension not in allowed list: {config.ALLOWED_EXTENSIONS}"
			if filename:
				res, respStatus =  AWS.putFileInBucket(filename, bucketName)
		return Response(json.dumps({"text": res}), status=respStatus, content_type='application/json')
	elif request.method == 'DELETE':
		res, status =  AWS.deleteFileInBucket(filename, bucketName)
		return Response(json.dumps({"text": res}), status=status, content_type='application/json')
		
@app.route('/api/images/<imageName>', methods=['GET'])
def manageImages(imageName = ''):
	res = f"Image not found: {imageName}"
	respStatus = 404
	bucket = AWS.getBucket(config.BUCKET_NAME)
	fileObjs = AWS.getFileObjsFromBucket(bucket, imageName)
	if request.method == 'GET':
		res = AWS.downloadFileFromBucket(bucket, fileObjs[0])
		return send_file(res, mimetype='image/jpeg')