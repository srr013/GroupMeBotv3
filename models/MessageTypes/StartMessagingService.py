import models.MessageTypes._DefaultMessageType as Default
import logging

class StartMessagingService(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText = ['start']
        self.responseType = 'text'
        self.responseText = ''
        self.isQualified = False
        self.helpText = "--start: start the messaging service, which allows Bot to send messages."

    def constructResponseText(self, payload, response):
        responseText = """
        Bot service activated. The bot will send responses per bot configuration.
        """
        return responseText

    def updateGroup(self):
        self.group.messagingServiceStatus = True