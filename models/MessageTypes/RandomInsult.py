import models.MessageTypes._DefaultMessageType as Default
import logging
import random
import responseText.insults as insults

class RandomInsult(Default.DefaultMessageType):
    def __init__(self):
        super().__init__()
        self.qualifyingText =['insult']
        self.qualifyingPercent = 100
        self.responseType = 'mention'
        self.messageCategory = 'random'

    def constructResponseText(self, payload, response):
        m = insults.insults[random.randint(0,len(insults.insults)-1)]
        #get the grammar right
        a = 'a'
        if m[0].lower() in ['a','e','i','o','u']:
            a = 'an'
        #add a second insult to string
        if random.randint(0, 99) > 50:
            if " " not in m:
                m+= " " + insults.insults[random.randint(0,len(insults.insults)-1)]
        return "@"+payload.get("name") + " is "+a+" "+ m