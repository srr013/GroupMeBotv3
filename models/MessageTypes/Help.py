import models.MessageTypes._DefaultMessageType as Default

class Help(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText = ['help']
        self.responseType = 'text'
    
    def constructResponseText(self, payload, response):
        responseText = """
        The following commands are supported:

        """
        for messageType in self.group.messageObjectList:
            responseText += messageType.helpText + "\n"

        return responseText