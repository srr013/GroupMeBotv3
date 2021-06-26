import requests
import logging
import random
import json

class Response():
    def __init__(self, group, payload):
        self.messageObject = ''
        self.group = group
        self.inboundMessagePayload = payload
        self.sendMessage = payload.get("sendMessage", True)
        self.messageObject = {}

    def send(self, responseText):
        statusCode = 0
        res = ''
        if self.messageObject:
            url = 'https://api.groupme.com/v3/bots/post'
            body = {}
            if self.messageObject.responseType == 'mention':
                body = {'bot_id': self.group.group.botId,
                        'text': responseText,
                        'attachments': [
                            {"type": "mentions",
                            "loci": self.get_message_loci(responseText),
                            "user_ids": self.group.memberIds}
                        ]
                    }
            elif self.messageObject.responseType == 'text':
                body = {
                    'bot_id': self.group.group.botId,
                    'text': responseText
                }
            if self.inboundMessagePayload.get("sendMessage", True):
                resp = requests.post(url, json=body)
                res = ''
                statusCode = resp.status_code
                if resp.status_code == 202:
                    res = "Message sent: "+responseText
                else:
                    res = "Message failed to post: "+ str(resp.status_code)
            else:
                res = "Message not sent due to sendMessage Paramter. Message: "+responseText
        else:
            res = "No message object set in response"
        logging.warn(res)
        return res, statusCode

    def get_message_loci(self, responseText):
        loci = []
        for name in self.group.memberNicknames:
            start = responseText.find(name)
            if start:
                end = start + len(name)
                #logging.warning("Loci are: " + start +" " +end])
                loci.append([start, end])
        return loci