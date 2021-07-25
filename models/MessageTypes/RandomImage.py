import models.MessageTypes._DefaultMessageType as Default
import logging
import os
import random
import responseText.images as images

class RandomImage(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText =['image']
        self.qualifyingPercent = 20
        self.responseType = 'image'
        self.messageCategory = 'random'
        self.helpText = '--image: bot will send a random image'

    def constructResponseText(self, payload, response):
        m = os.path.join("static","images", images.meme_files[random.randint(0, len(images.meme_files)-1)])
        return m

    def updateGroup(self):
        self.group.counter_current = 0
        self.group.counter_currentThreshold = random.randint(self.group.counter_lowerBound, self.group.counter_upperBound)
        return