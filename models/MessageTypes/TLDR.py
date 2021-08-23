import models.MessageTypes._DefaultMessageType as Default
import logging
import random
from responseText.tldr import tldr

class TLDR(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText =['tldr']
        self.responseType = 'command'
        self.helpText = "--tldr: trigger a response from the bot due to a long message"
        
    def qualifyText(self, text):
        if text.count(' ') > 100:
            return True
        if self.qualifyingText:
            for m in self.qualifyingText:
                l = ["--"+m, "-"+m, "\u2014"+m]
                for message in l:
                    if message in text.lower():
                        return True
        return False

    def constructResponseText(self, payload, response):
        m = tldr[random.randint(0,len(tldr)-1)]
        return m

