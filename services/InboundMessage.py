
import importlib
import random
import logging
import json
import services.Response as Response
import services.config as config

import models.MessageTypes.Help as Help
import models.MessageTypes.MentionAll as MentionAll
import models.MessageTypes.MessagingServiceStatus as MessagingServiceStatus
import models.MessageTypes.RandomHouseDraw as RandomHouseDraw
import models.MessageTypes.RandomInsult as RandomInsult
import models.MessageTypes.StartMessagingService as StartMessagingService
import models.MessageTypes.StopMessagingService as StopMessagingService

# messageModuleList = [
#     'Help', 
#     'MentionAll', 
#     'MessagingServiceStatus', 
#     'RandomHouseDraw', 
#     'RandomInsult', 
#     'StartMessagingService', 
#     'StopMessagingService'
#     ]

# messageObjectList = []
# for messageType in messageModuleList:
#     messageObjectList.append(eval("%s.%s()" % (messageType, messageType)))

def parseMessageContent(payload, group, response, bot):
    messageModuleList = []
    inboundMessage = payload.get('text')

    if validateGroupmePost(payload):
        #create the message type modules and 
        #check if inbound text meets any qualifyingText parameters
        group.messageObjects = group.group.getMessageObjects()

        for m in group.messageObjects:
            #check for a command and process only the first command
            if m.qualifyText(inboundMessage):
                return m
    return {}






def validateGroupmePost(payload, allowBot=False):
    isValid = False
    if allowBot:
        if payload.get('sender_type') != "system"\
            and payload.get('text') \
                and payload.get('group_id') \
                    and payload.get("source_guid"):
            isValid = True
    else:
        if payload.get('sender_type') not in ["bot", "system"] \
            and payload.get('sender_type') \
                and payload.get('group_id') \
                    and payload.get('text')  \
                        and payload.get("source_guid"):
            isValid = True
    return isValid

def isBotOrSystemMessage(payload):
    if payload.get('sender_type') in ["bot", "system"]:
        return True
    return False