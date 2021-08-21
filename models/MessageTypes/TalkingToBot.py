import models.MessageTypes._DefaultMessageType as Default
import logging
import random
from responseText.talkingToBot import talkingToBot

class TalkingToBot(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText =['talkingToBot']
        self.responseType = 'text'
        self.helpText = "--talkingToBot: trigger a response from the bot based on a mention of Bot's name"
        
    def qualifyText(self, inboundMessage):
        if self.group.bot:
            if self.group.bot.botName.lower() in inboundMessage.lower():
                return True
        if self.qualifyingText:
            for m in self.qualifyingText:
                m = m.lower()
                l = ["--"+m, "-"+m, "\u2014"+m]
                for message in l:
                    if message in inboundMessage.lower():
                        return True
        return False

    def constructResponseText(self, payload, response):
        m = talkingToBot[random.randint(0,len(talkingToBot)-1)]
        return m

