import models.MessageTypes._DefaultMessageType as Default
import logging

class MentionAll(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText = ['@all']
        self.responseType = 'mention'
        self.helpText = "@all: tag all users in the GroupMe"

    def qualifyText(self, text):
        if self.qualifyingText:
            for m in self.qualifyingText:
                if m in text.lower():
                    return True
        return False

    def constructResponseText(self, payload, response):
        start_text, end_text = self.get_surrounding_text(payload.get('text'))
        mentions = self.create_mention_text(response)
        return start_text + ' '+ mentions + ' '+ end_text


    def get_surrounding_text(self, text):
        l = text.lower()
        start_index = l.find("@all")
        start_text = ""
        if start_index > 0:
            start_text = text[0:start_index]
        end_index = start_index + 4
        end_text = text[end_index+1:len(text)]
        return start_text, end_text

    def create_mention_text(self, response):
        msg = ""
        for name in response.groupMeGroup.memberNicknames:
            msg += "@"+name+", "
        msg = msg[0:-2]
        return msg

