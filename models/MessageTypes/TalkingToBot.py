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
        self.content = talkingToBot

    def qualifyText(self, text):
        if self.group.bot:
            if self.group.bot.botName.lower() in text.lower():
                return True
            if 'insultbot' in text.lower():
                return True
            if 'insult bot' in text.lower():
                return True
        if self.qualifyingText:
            for m in self.qualifyingText:
                m = m.lower()
                l = ["--"+m, "-"+m, "\u2014"+m]
                for message in l:
                    if message in text.lower():
                        return True
        return False

    def constructResponseText(self, payload, response):
        self.messageSourceIndex = random.randint(0,len(self.content)-1)
        m = self.content[self.messageSourceIndex]['text']
        return m

