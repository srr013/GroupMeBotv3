
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

def parseMessage(request, group):
    messageModuleList = []
    logging.warn("Request: "+json.dumps(request.get_json()))
    payload = request.get_json()
    inboundMessage = payload.get('text')
    response = Response.Response(group, payload)
    if validateGroupmePost(payload):
        group.group.counter_current += 1
        #create the message type modules and 
        #check if inbound text meets any qualifyingText parameters
        group.messageObjects = group.group.getMessageObjects()
        for m in group.messageObjects:
            #check for a command and process only the first command
            if m.qualifyText(inboundMessage):
                response.messageObject = m
        if not response.messageObject:
        #No commands were provided, checking for random message
        #assign each module that has a qualifying percent a number range
            if group.readyForMessage():
                for m in group.messageObjects:
                    #set the random selection range for each message type
                    randUpperBound = m.getRandBoundary(0)
                #select the random #
                selector = random.randint(0, randUpperBound)
                for m in group.messageObjects:
                    #if the selected number falls within random selection range
                    if m.randLowerBound <= selector <= m.randUpperBound:
                        response.messageObject = m

        #send the queued message
        if response.messageObject:
            responseText = response.messageObject.constructResponseText(payload, response)
            response.messageObject.updateGroup(group)
            res, respStatus = response.send(responseText)
    else:
        res = "Group not found"

        respStatus = 404
    return res, respStatus


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