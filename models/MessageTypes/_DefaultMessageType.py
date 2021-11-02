from operator import index
import random
import os
import json
import datetime
from werkzeug.utils import secure_filename
import services.config as config
import services.aws as AWS

class DefaultMessageType():
    def __init__(self, group):
        self.qualifyingText = []
        self.qualifyingPercent = 0 #number from 1 - 100
        self.qualifyingKey = None
        self.responseType = 'text'
        self.responseText = ''
        self.isQualified = False
        self.group = group

        self.messageCategory = "command"
        self.randUpperBound = 0
        self.randLowerBound = 0
        self.typeDefinition = {
            "name": self.__class__.__name__,
            "active": True,
            "action": ''
        }
        self.helpText = ''
        #self.followUpAction = '' #persists a state across message transmissions for a specific message type
        self.messageSourceIndex = None #persist (single session) the index of the message from the list of available messages
        self.randomizeResponseChance = 0
        self.content = []
        self.doNotDecrement = False

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
        return ''
    
    def setContent(self):
        if self.group.s3Content:
            if self.group.s3Content['text'].get(self.__class__.__name__):
                content = self.group.s3Content['text'].get(self.__class__.__name__)
                if isinstance(content, list):
                    self.content = []
                    previouslyUsedContent = []
                    #set self.content just to unused content
                    for c in content:
                        if c.get('lastUsedDate') == '':
                            self.content.append(c)
                        else:
                            previouslyUsedContent.append(c)
                    #recycle content if all is already used
                    if not self.content:
                        self.content = previouslyUsedContent
                        for c in content:
                            c['lastUsedDate'] = ''
                # elif isinstance(content, dict):
                #     self.content = {}
                #     previouslyUsedContent = {}
                #     #set self.content just to unused content
                #     for k in content.keys():
                #         for c in k:
                #             if c.get('lastUsedDate') == '':
                #                 if isinstance(self.content.get(k), list):
                #                     self.content[k].append(c)
                #                 else:
                #                     self.content[k] = [c]
                #             else:
                #                 if isinstance(previouslyUsedContent.get(k), list):
                #                     previouslyUsedContent[k].append(c)
                #                 else:
                #                     previouslyUsedContent[k] = [c]
                #     #recycle content if all is already used
                #     if not self.content:
                #         self.content = previouslyUsedContent
                #         for c in content:
                #             c['lastUsedDate'] = ''

                    

    def performFollowUp(self):
        pass

    def updateGroupData(self):
        self.setMessageLastUsedDate()
        self.updateGroup()

    def updateGroup(self):
        #used by children to update the group's settings via message commands
        pass

    def setMessageLastUsedDate(self):
        if not self.doNotDecrement:
            if self.messageSourceIndex != None and self.qualifyingKey == None:
                fileName = self.__class__.__name__+".json"
                self.content[self.messageSourceIndex]['lastUsedDate'] = datetime.datetime.today().strftime("%Y-%m-%d")
                local_filepath = os.path.join(config.UPLOAD_FOLDER, self.group.groupId, "text", fileName)
                with open(local_filepath, "w+") as f:
                    f.write(json.dumps(self.content))
                aws_filepath = secure_filename(os.path.join(self.group.groupId, "text", fileName))
                res, respStatus =  AWS.putFileInBucket(secure_filename(local_filepath), config.BUCKET_NAME, aws_filepath)
        # elif self.messageSourceIndex != None and self.qualifyingKey != None:
        #     fileName = self.__class__.__name__+".json"
        #     self.content[self.qualifyingKey][self.messageSourceIndex]['lastUsedDate'] = datetime.datetime.today().strftime("%Y-%m-%d")
        #     local_filepath = os.path.join(config.UPLOAD_FOLDER, self.group.groupId, "text", fileName)
        #     with open(local_filepath, "w+") as f:
        #         f.write(json.dumps(self.content))
        #     aws_filepath = secure_filename(os.path.join(self.group.groupId, "text", fileName))
        #     res, respStatus =  AWS.putFileInBucket(secure_filename(local_filepath), config.BUCKET_NAME, aws_filepath)


    def getRandBoundary(self, randUpperBound):
        self.randLowerBound = randUpperBound
        self.randUpperBound = randUpperBound + self.qualifyingPercent
        return self.randUpperBound

    def randomizeChanceToSendMessage(self):
        if self.randomizeResponseChance:
            rand  = random.randint(0,100)
            if rand < self.randomizeResponseChance:
                return True
        return False


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