import requests
import json
import logging
import os
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app import db
import services.config as config
import random

import models.MessageTypes.Help as Help
import models.MessageTypes.MentionAll as MentionAll
import models.MessageTypes.MessagingServiceStatus as MessagingServiceStatus
import models.MessageTypes.RandomHouseDraw as RandomHouseDraw
import models.MessageTypes.RandomInsult as RandomInsult
import models.MessageTypes.StartMessagingService as StartMessagingService
import models.MessageTypes.StopMessagingService as StopMessagingService
import models.MessageTypes.RandomEncouragement as RandomEncouragement
import models.MessageTypes.RandomImage as RandomImage
import models.MessageTypes.TalkingToBot as TalkingToBot
import models.MessageTypes.TLDR as TLDR
import models.MessageTypes.FewerAndLess as FewerAndLess
import models.MessageTypes.messageTypes as systemMessageTypes

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    groupId = db.Column(db.String(), unique=True)
    groupName = db.Column(db.String())
    botId = db.Column(db.String(), ForeignKey('bots.id'))
    counter_lowerBound = db.Column(db.Integer)
    counter_upperBound = db.Column(db.Integer)
    counter_currentThreshold = db.Column(db.Integer)
    counter_current = db.Column(db.Integer)
    messageTypes = db.Column(JSON)
    active = db.Column(db.Boolean)
    messagingServiceStatus = db.Column(db.Boolean)
    # creatingUser = db.Column(db.Integer)
    # users = db.Column(ARRAY(db.Integer, ForeignKey('users.id')))
    bot = relationship("Bot", back_populates="group")
    inboundMessage = relationship("InboundMessage", back_populates="group")
    # user_id = relationship("User", back_populates="groups")


    def __init__(self, groupId, botId, groupName, payload={}):
        self.groupId = groupId if groupId else payload.get('groupId')
        self.groupName = groupName if groupName else payload.get('groupName', "default")
        self.botId = botId if botId else payload.get('botId')
        self.counter_lowerBound = payload.get('counter_lowerBound', 10)
        self.counter_upperBound = payload.get('counter_upperBound', 15)
        self.counter_currentThreshold = payload.get('counter_currentThreshold', self.counter_lowerBound)
        self.counter_current = payload.get('counter_current', 0)
        self.active = payload.get('active', True)
        self.messagingServiceStatus = payload.get('messagingServiceStatus', True)
        self.messageTypes = payload.get('messageTypes', {})
        self.messageObjectList = []


    def __repr__(self):
        return '<id {}>'.format(self.id)

    def createGroupData(self):
        self.setMessageTypes()

    def initializeGroupData(self):
        if self.counter_current > self.counter_currentThreshold:
            self.counter_current = 0
            self.counter_currentThreshold = random.randint(self.counter_lowerBound, self.counter_upperBound)
        if isinstance(self.messageTypes, str):
            self.messageTypes = json.loads(self.messageTypes)
        self.getMessageObjects()

    def getMessageObjects(self):
        messageObjectList = []
        for messageType in systemMessageTypes.types:
            module = eval("%s.%s(self)" % (messageType, messageType))
            for mType in self.messageTypes:
                if mType.get('name') == module.__class__.__name__ and mType.get('active'):
                    messageObjectList.append(module)
        self.messageObjectList = messageObjectList
        return messageObjectList

    def setMessageTypes(self):
        messageTypeList = []
        for messageType in systemMessageTypes.types:
            module = eval("%s.%s(self)" % (messageType, messageType))
            messageTypeList.append(module.typeDefinition)
        self.messageTypes = json.dumps(messageTypeList)

    def deserialize(self):
        group = {
            "id": self.id,
            "groupName": self.groupName,
            "groupId": self.groupId,
            "botId": self.botId,
            "messageTypes": self.messageTypes,
            "messagingServiceStatus": self.messagingServiceStatus,
            "Message Counter": str(self.counter_current) +"/"+ str(self.counter_currentThreshold),
            "Message Counter Bounds": str(self.counter_lowerBound) +"/"+ str(self.counter_upperBound)
        }
        return group
