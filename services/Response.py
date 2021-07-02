import requests
import logging
import random
import json

class Response():
    def __init__(self, group, payload):
        self.messageObject = ''
        self.groupMeGroup = group
        self.inboundMessagePayload = payload
        self.sendMessage = payload.get("sendMessage", True)
        self.messageObject = {}
        self.responseText = "No content set"


    def getTriggeredResponse(self, group):
        #No commands were provided, checking for random message
        #assign each module that has a qualifying percent a number range
        for m in group.messageObjects:
            #set the random selection range for each message type
            randUpperBound = m.getRandBoundary(0)
        #select the random #
        selector = random.randint(0, randUpperBound)
        for m in group.messageObjects:
            #if the selected number falls within random selection range
            if m.randLowerBound <= selector <= m.randUpperBound:
                return m

    def send(self):
        statusCode = 0
        res = ''
        if self.messageObject:
            url = 'https://api.groupme.com/v3/bots/post'
            body = {}
            if self.messageObject.responseType == 'mention':
                body = {'bot_id': self.groupMeGroup.group.botId,
                        'text': self.responseText,
                        'attachments': [
                            {"type": "mentions",
                            "loci": self.get_message_loci(),
                            "user_ids": self.groupMeGroup.memberIds}
                        ]
                    }
            elif self.messageObject.responseType == 'text':
                body = {
                    'bot_id': self.groupMeGroup.group.botId,
                    'text': self.responseText
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
        for name in self.groupMeGroup.memberNicknames:
            start = self.responseText.find(name)
            if start:
                end = start + len(name)
                #logging.warning("Loci are: " + start +" " +end])
                loci.append([start, end])
        return loci