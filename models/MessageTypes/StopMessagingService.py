import models.MessageTypes._DefaultMessageType as Default
import logging

class StopMessagingService(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText = ['stop']
        self.responseType = 'text'
        self.responseText = ''
        self.isQualified = False
        self.helpText = "--start: start the messaging service, which allows Bot to send messages. Bot will always respond to --commands."

    def constructResponseText(self, payload, response):
        responseText = """
        Bot service deactivated. Messages will monitored but no further messages will be sent.
        """
        return responseText

    def updateGroup(self):
        self.group.messagingServiceStatus = False