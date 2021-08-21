import models.MessageTypes._DefaultMessageType as Default
import logging
import random

class SendMessageFromAPI(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.responseType = 'text'
        #this is not a standard message object as it is not associated to a group and only used via API

    def constructResponseText(self, payload, response):
        return payload.get('message')


