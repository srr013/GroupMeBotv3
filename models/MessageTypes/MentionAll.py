import models.MessageTypes._DefaultMessageType as Default
import logging

class MentionAll(Default.DefaultMessageType):
    def __init__(self):
        super().__init__()
        self.qualifyingText = ['@all']
        self.responseType = 'mention'

    def qualifyText(self, inboundMessage):
        if self.qualifyingText:
            for m in self.qualifyingText:
                if m in inboundMessage.lower():
                    return True
        return False

    def constructResponseText(self, payload, response):
        start_text, end_text = self.get_surrounding_text(payload.get('text'))
        mentions = self.create_mention_text(response)
        return start_text + ' '+ mentions + ' '+ end_text


    def get_surrounding_text(self, inboundMessage):
        l = inboundMessage.lower()
        start_index = l.find("@all")
        start_text = ""
        if start_index > 0:
            start_text = inboundMessage[0:start_index]
        end_index = start_index + 4
        end_text = inboundMessage[end_index+1:len(inboundMessage)]
        return start_text, end_text

    def create_mention_text(self, response):
        msg = ""
        for name in response.groupMeGroup.memberNicknames:
            msg += "@"+name+", "
        msg = msg[0:-2]
        return msg

