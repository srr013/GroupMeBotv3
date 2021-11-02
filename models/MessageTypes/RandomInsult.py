import models.MessageTypes._DefaultMessageType as Default
import logging
import random
import responseText.insults as insults

class RandomInsult(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText =['insult']
        self.qualifyingPercent = 10
        self.responseType = 'mention'
        self.messageCategory = 'random'
        self.helpText = '--insult: bot will send a random insult about you'
        self.content = insults.insults

    def constructResponseText(self, payload, response):
        self.messageSourceIndex = random.randint(0,len(self.content)-1)
        responseObj = self.content[self.messageSourceIndex]
        m = responseObj['text']
        addUser = random.randint(1,2)
        if addUser % 2 == 0:
            #get the grammar right
            a = 'a'
            if m[0].lower() in ['a','e','i','o','u']:
                a = 'an'
            #add a second insult to string
            if random.randint(0, 99) > 50:
                if " " not in m:
                    m+= " " + self.content[random.randint(0,len(self.content)-1)]['text']
            return "@"+payload.get("name") + " is "+a+" "+ m
        else:
            self.responseType = 'text'
            return m

    def updateGroup(self):
        self.group.counter_current = 0
        self.group.counter_currentThreshold = random.randint(self.group.counter_lowerBound, self.group.counter_upperBound)
        return