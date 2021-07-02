import requests
import json
import logging
import os
from sqlalchemy.dialects.postgresql import JSON
import services.config as config

class GroupmeGroup():
    def __init__(self, group):
        self.group = group
        self.rawData = self.getRawData()

        if self.rawData:
            self.data = json.loads(self.rawData.text)
            if self.data.get("response"):
                self.memberNicknames = self.getMembers()
                self.memberIds = self.getMemberIds()
                self.memberNames = self.getNames()
                self.groupName = self.data['response']['name']
                if not self.group.groupName:
                    self.group.groupName = self.groupName
        else:
            logging.error("Group creation failed: Could not retrieve or parse GroupMe API data")
        self.messageObjects = []

    def __repr__(self):
        return '<id {}>'.format(self.group.id)

    def getRawData(self):
        url = "https://api.groupme.com/v3/groups/" + self.group.groupId + "?token="+config.GROUPME_ACCESS_TOKEN
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            return {}
    
    def getMembers(self):
        members = []
        for member in self.data["response"]["members"]:
            members.append(member['nickname'])
        return members
        
        
    def getMemberIds(self):
        memberIds = []
        for member in self.data["response"]["members"]:
            memberIds.append(member['user_id'])
        return memberIds

    def getNames(self):
        names = []
        for member in self.data["response"]["members"]:
            names.append(member['name'])
        return names

    def getMemberNamesFromInput(self, input):
        text = input.lower()
        text.split(",")
        names = []
        if isinstance(text, str): #used for single person group
            text = [text]
        for p in text:
            for member in self.memberNames:
                logging.warn('P: {}, Member: {}'.format(p, member))
                if p in member.lower():
                    names.append(member)
        if len(names) != len(text):
            logging.warn("Name matching on GroupMe Names failed. Returning name list as-is")
            names = text
        return names

    def readyForMessage(self):
        #if messaging is on
        if self.group.messagingServiceStatus:
            if self.group.counter_current >= self.group.counter_currentThreshold:
                return True
        return False


