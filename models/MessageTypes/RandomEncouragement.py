import models.MessageTypes._DefaultMessageType as Default
import logging
import random
import responseText.encouragement as encouragement

class RandomEncouragement(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText =['encourage', 'encouragement']
        self.qualifyingPercent = 20
        self.responseType = 'text'
        self.messageCategory = 'random'
        self.helpText = '--encourage: bot will send you a pick-me-up'

    def constructResponseText(self, payload, response):
        m = encouragement.encouragement[random.randint(0,len(encouragement.encouragement)-1)]
        return m

    def updateGroup(self):
        self.group.counter_current = 0
        self.group.counter_currentThreshold = random.randint(self.group.counter_lowerBound, self.group.counter_upperBound)
        return