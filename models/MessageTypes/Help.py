import models.MessageTypes._DefaultMessageType as Default

class Help(Default.DefaultMessageType):
    def __init__(self):
        super().__init__()
        self.qualifyingText = ['help']
        self.responseType = 'text'
    
    def constructResponseText(self, payload, response):
        responseText = """
        The following commands are supported:
        @all - tag all users in the GroupMe
        --randomhouses <gamename> <userlist:comma-delimited>
        ex: --randomhouses 3p scott,steve,maulik
        supported games: RTKL, NKFD, RITS, SITN, 3p
        If the game size does not match the number of groupme members then you must specify the members to include
        Don't include spaces in the message except between parameters
        Player names should be separated by commas
        """
        return responseText