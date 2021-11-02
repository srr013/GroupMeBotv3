import models.MessageTypes._DefaultMessageType as Default
import logging
import os
import random
import services.aws as aws
import responseText.images as images

class RandomImage(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText =['image']
        self.qualifyingPercent = 20
        self.responseType = 'image'
        self.messageCategory = 'random'
        self.helpText = '--image: bot will send a random image'
        self.content = images.meme_files

    def constructResponseText(self, payload, response):
        self.messageSourceIndex = random.randint(0,len(self.content)-1)
        objName = self.content[self.messageSourceIndex]['text']
        obj = ''
        for i in self.group.s3Content['images']:
            fileName = i['Key'].split("/")[2]
            if fileName == objName:
                obj = i
                break
        if i and obj:
            if not self.group.s3Content:
                m = os.path.join("static","images", objName)
            else:
                m = aws.downloadFileFromBucket({'Name': self.group.s3Content['Name']}, obj)
            return m
        return "None"

    def updateGroup(self):
        self.group.counter_current = 0
        self.group.counter_currentThreshold = random.randint(self.group.counter_lowerBound, self.group.counter_upperBound)
        return