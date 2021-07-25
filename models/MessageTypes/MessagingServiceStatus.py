import models.MessageTypes._DefaultMessageType as Default
import logging

class MessagingServiceStatus(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText = ['status']
        self.responseType = 'text'
        self.helpText = "--status: get the Bot's current messaging statuses"

    def constructResponseText(self, payload, response):
        messagingStatusBool = 'On' if self.group.messagingServiceStatus else 'Off'
        messagingStatusVerb = 'will' if self.group.messagingServiceStatus else 'will not'
        return f"""Bot is always listening 8^). Delete to completely deactivate.\n Messaging Service is {messagingStatusBool}. I {messagingStatusVerb} send random messages. I always reply to commands.
            """