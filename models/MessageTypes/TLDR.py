import models.MessageTypes._DefaultMessageType as Default
import logging
import random
from responseText.tldr import tldr

class TLDR(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText =['tldr']
        self.responseType = 'text'
        self.helpText = "--tldr: trigger a response from the bot due to a long message"
        self.content = tldr

    def qualifyText(self, text):
        if text.count(' ') > 80:
            return True
        if self.qualifyingText:
            for m in self.qualifyingText:
                l = ["--"+m, "-"+m, "\u2014"+m]
                for message in l:
                    if message in text.lower():
                        return True
        return False

    def constructResponseText(self, payload, response):
        self.messageSourceIndex = random.randint(0,len(self.content)-1)
        m = self.content[self.messageSourceIndex]['text']
        return m

