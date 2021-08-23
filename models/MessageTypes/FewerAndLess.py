import models.MessageTypes._DefaultMessageType as Default
import logging

class FewerAndLess(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText = [' fewer ', ' less ']
        self.responseType = 'text'
        self.messageCategory = "command"

    def qualifyText(self, text):
        if self.qualifyingText:
            for m in self.qualifyingText:
                if m in text.lower():
                    return True
        return False

    def constructResponseText(self, payload, response):
        msg = '*fewer'
        if ' fewer ' in payload.get('text'):
            return '*less'
        return msg


