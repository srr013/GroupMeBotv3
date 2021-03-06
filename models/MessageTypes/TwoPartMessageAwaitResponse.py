from sqlalchemy.sql.elements import Null
from sqlalchemy.orm.attributes import flag_modified
import models.MessageTypes._DefaultMessageType as Default
import logging
import random
from responseText.TwoPartMessageAwaitResponse import responses as TwoPartMessageAwaitResponse

class TwoPartMessageAwaitResponse(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText =['twoPartMessageAwaitResponse']
        self.responseType = 'text'
        self.qualifyingPercent = 10
        self.messageCategory = 'random'
        self.helpText = "--TwoPartMessageAwaitResponse: Bot sends a message and awaits response from the group before sending another"
        self.content = TwoPartMessageAwaitResponse

    def qualifyText(self, text):
        if self.qualifyingText:
            for m in self.qualifyingText:
                m = m.lower()
                l = ["--"+m, "-"+m, "\u2014"+m]
                for message in l:
                    if message in text.lower():
                        return True
        return False

    def constructResponseText(self, payload, response):
        if self.messageSourceIndex == None:
            self.messageSourceIndex = random.randint(0,len(self.content)-1)
            m = self.content[self.messageSourceIndex]['text'][0]
            self.doNotDecrement = True
        else:
            m = self.content[int(self.messageSourceIndex)]['text'][1]
        return m

    def updateGroup(self):
        for messageType in self.group.messageTypes:
            if messageType['name'] == "TwoPartMessageAwaitResponse":
                if messageType.get('action', None) is not None:
                    messageType.pop('action')
                else:
                    messageType['action'] = self.messageSourceIndex
        flag_modified(self.group, "messageTypes") #required to force change to jsonB DB column
