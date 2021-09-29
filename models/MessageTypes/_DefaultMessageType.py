from operator import index
import random

class DefaultMessageType():
    def __init__(self, group):
        self.qualifyingText = []
        self.qualifyingPercent = 0 #number from 1 - 100
        self.responseType = 'text'
        self.responseText = ''
        self.isQualified = False
        self.group = group

        self.messageCategory = "command"
        self.randUpperBound = 0
        self.randLowerBound = 0
        self.typeDefinition = {
            "name": self.__class__.__name__,
            "active": True
        }
        self.helpText = ''
    
    def qualifyText(self, text):
        if self.qualifyingText:
            for m in self.qualifyingText:
                l = ["--"+m, "-"+m, "\u2014"+m]
                for message in l:
                    if message in text.lower():
                        return True
        return False
    
    def constructResponseText(self, payload, response):
        return ''
    
    def updateGroupData(self):
        self.updateGroup()

    def updateGroup(self):
        #used by children to update the group's settings via message commands
        pass

    def getRandBoundary(self, randUpperBound):
        self.randLowerBound = randUpperBound
        self.randUpperBound = randUpperBound + self.qualifyingPercent
        return self.randUpperBound

    def stringIsWordInText(self, key, text):
        if key in text:
            if " " + key + " " in text: #is it a standalone word?
                return True
            elif text.index(key) == 0 and key+" " in text: #is it the first word followed by others?
                return True
            elif text.index(key) == len(text)-len(key) and " "+key in text: #is it the last word?
                return True
            elif text.index(key) == 0 and len(text) == len(key): #is it the only word in the message?
                return True
        return False