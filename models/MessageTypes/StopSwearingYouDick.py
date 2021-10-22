import models.MessageTypes._DefaultMessageType as Default
import logging
import random
from responseText.stopSwearing import stopSwearing

class StopSwearingYouDick(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText =['StopSwearingYouDick']
        self.responseType = 'text'
        self.helpText = f"--StopSwearingYouDick: triggered when you say the following words: {[k for k in stopSwearing.keys()]}"
        self.qualifyingKey = ''
        self.randomizeResponseChance = 60

    def qualifyText(self, text):
        returnVal = False
        for key in stopSwearing.keys():
            if self.stringIsWordInText(key, text):
                self.qualifyingKey = key
                return True
        if self.qualifyingText:
            for m in self.qualifyingText:
                m = m.lower()
                l = ["--"+m, "-"+m, "\u2014"+m]
                for message in l:
                    if message in text.lower():
                        returnVal = True
        if returnVal:
            returnVal = self.randomizeChanceToSendMessage()
            
        return returnVal

    def constructResponseText(self, payload, response):
        key = self.qualifyingKey
        if not key:
            keys = stopSwearing.keys()
            key = keys[random.randint(0,len(stopSwearing.keys())-1)]
        vals = stopSwearing[key]
        return vals[random.randint(0,len(vals)-1)]

