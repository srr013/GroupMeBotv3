import models.MessageTypes._DefaultMessageType as Default
import logging

class MessagingServiceStatus(Default.DefaultMessageType):
    def __init__(self):
        super().__init__()
        self.qualifyingText = ['status']
        self.responseType = 'text'

    def constructResponseText(self, payload, response):
        s = 'On' if response.groupMeGroup.messagingServiceStatus else 'Off'
        return "Bot service is: " + s