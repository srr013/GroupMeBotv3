import models.MessageTypes._DefaultMessageType as Default
import logging
import random
import responseText.encouragement as encouragement

class RandomEncouragement(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText =['encourage', 'encouragement']
        self.qualifyingPercent = 10
        self.responseType = 'text'
        self.messageCategory = 'random'
        self.helpText = '--encourage: bot will send you a pick-me-up'
        self.content = encouragement.encouragement

    def constructResponseText(self, payload, response):
        self.messageSourceIndex = random.randint(0,len(self.content)-1)
        m = self.content[self.messageSourceIndex]['text']
        return m

    def updateGroup(self):
        self.group.counter_current = 0
        self.group.counter_currentThreshold = random.randint(self.group.counter_lowerBound, self.group.counter_upperBound)
        return