import models.MessageTypes._DefaultMessageType as Default
import logging

class StopMessagingService(Default.DefaultMessageType):
    def __init__(self):
        super().__init__()
        self.qualifyingText = ['stop']
        self.responseType = 'text'
        self.responseText = ''
        self.isQualified = False

    def constructResponseText(self, payload, response):
        responseText = """
        Bot service deactivated. Messages will monitored but no further messages will be sent.
        """
        return responseText

    def updateGroup(self, group):
        group.messagingServiceStatus = False