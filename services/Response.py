import requests
import logging
import random
import json
import os
import services.config as config


class Response():
    def __init__(self, group, payload):
        self.messageObject = ''
        self.groupMeGroup = group
        self.inboundMessagePayload = payload #payload may be empty
        self.sendMessage = payload.get("sendMessage", True)
        self.messageObject = {}
        self.responseText = "No content set"


    def getRandomCategoryResponse(self, group):
        #No commands were provided, checking for random message
        #assign each module that has a qualifying percent a number range
        messageObjects = []
        randUpperBound = 0
        for m in group.messageObjects:
            #set the random selection range for each message type
            if m.messageCategory == 'random':
                messageObjects.append(m)
                randUpperBound = m.getRandBoundary(randUpperBound)
        #select the random #
        if randUpperBound > 0:
            selector = random.randint(0, randUpperBound)
            for m in messageObjects:
                #if the selected number falls within random selection range
                if m.randLowerBound <= selector <= m.randUpperBound:
                    return m

    #Returns a message object, based on a qualification, to be used in response creation
    def checkMessageForQualifyingAttributes(self, inboundMessage, groupMeGroup):
        messageModuleList = []
        if inboundMessage.validateGroupmePost():
            #create the message type modules and 
            #check if inbound text meets any qualifyingText parameters
            groupMeGroup.messageObjects = groupMeGroup.group.getMessageObjects()

            for m in groupMeGroup.messageObjects:
                #check for a command and process only the first command
                if m.qualifyText(inboundMessage.messageText):
                    return m
                #check the messageType JSON data stored for the group
                for messageType in groupMeGroup.group.messageTypes:
                    #finds the appropriate messageType and sets an action within it for use in response construction
                    #allows storage of a follow-up command for a given message type across messages
                    if messageType.get('action', None) is not None and messageType['name'] == m.__class__.__name__:
                        m.followUpAction = messageType['action']
                        return m
        return {}



    def send(self):
        statusCode = 0
        res = ''
        if self.messageObject:
            url = 'https://api.groupme.com/v3/bots/post'
            body = {}
            if self.messageObject.responseType == 'mention':
                loci, memberIds = self.get_message_loci()
                body = {'bot_id': self.groupMeGroup.group.botId,
                        'text': self.responseText,
                        'attachments': [
                            {"type": "mentions",
                            "loci": loci,
                            "user_ids": memberIds}
                        ]
                    }
            elif self.messageObject.responseType == 'text':
                body = {
                    'bot_id': self.groupMeGroup.group.botId,
                    'text': self.responseText
                }
            #Send a message with an image attached in the groupchat
            elif self.messageObject.responseType == 'image':
                urlOnGroupMeService = self.upload_image_to_groupme(self.responseText)
                body = {
                    'bot_id'		: self.groupMeGroup.group.botId,
                    'text'			: '',
                    'picture_url'		: urlOnGroupMeService['payload']['url']
                }
            if self.inboundMessagePayload.get("sendMessage", True):
                resp = requests.post(url, json=body)
                res = ''
                statusCode = resp.status_code
                if resp.status_code == 202:
                    res = "Message sent: "+self.responseText
                else:
                    #Note - "requested path doesn't exist error might mean bot ID doesn't exist"
                    res = f"Response failed with {resp.status_code}: {resp.text}"
            else:
                res = "Message not sent due to sendMessage Paramter. Message: "+self.responseText
        else:
            res = "No message object set in response"
        logging.warn(res)
        return res, statusCode

    def get_message_loci(self):
        loci = []
        memberIds = []
        for member in self.groupMeGroup.members:
            start = self.responseText.find(member['nickname'])
            if start != -1:
                end = start + len(member['nickname'])
                #logging.warning("Loci are: " + start +" " +end])
                loci.append([start, end])
                memberIds.append(member['id'])
        return loci, memberIds
    
    #Uploads image to GroupMe's services and returns the new URL
    def upload_image_to_groupme(self, filename):
        headers = {'Content-Type': 'image/jpeg',
                    'X-Access-Token': config.GROUPME_ACCESS_TOKEN}
        url = 'https://image.groupme.com/pictures'
        data = open(filename, 'rb').read()
        r = requests.post(url, headers=headers, data=data)
        imageurl = json.loads(r.text)
        return imageurl