import requests
import json
import logging
import os

# def get_user_names_and_ids(groupme_access_token, group_id):
#     names = []
#     ids = []
#     url = "https://api.groupme.com/v3/groups/" + group_id + "?token="+groupme_access_token
#     response = requests.get(url)
#     logging.warn("Response: "+response.text)
#     response = json.loads(response.text)
#     if response.get("response"):
#         for member in response["response"]["members"]:
#             names.append(member['nickname'])
#             logging.warn("Name identified: "+ member['nickname'])
#             ids.append(member["user_id"])
#     return names, ids

class Group():
    def __init__(self, groupId, groupme_access_token):
        self.rawData = self.getRawData(groupId, groupme_access_token)
        self.groupType = "Test"
        self.gmBotId = os.environ.get('GM_BOT_ID_TEST')
        self.data = {}
        prdIds = ['60197068']
        if groupId in prdIds:
            self.gmBotId = os.environ.get('GM_BOT_ID')
        if self.rawData:
            self.data = json.loads(self.rawData.text)
            if self.data.get("response"):
                self.memberNicknames = self.getMembers()
                self.memberIds = self.getMemberIds()
                self.memberNames = self.getNames()
                
        else:
            logging.error("Could not retrieve or parse group API data")

    def getRawData(self, group_id, groupme_access_token):
        url = "https://api.groupme.com/v3/groups/" + group_id + "?token="+groupme_access_token
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
