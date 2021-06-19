import models.MessageTypes._DefaultMessageType as Default
import logging

class StartMessagingService(Default.DefaultMessageType):
    def __init__(self):
        super().__init__()
        self.qualifyingText = ['start']
        self.responseType = 'text'
        self.responseText = ''
        self.isQualified = False

    def constructResponseText(self, payload, response):
        responseText = """
        Bot service activated. The bot will send responses per bot configuration.
        """
        return responseText

    def updateGroup(self, group):
        group.messagingServiceStatus = True