import requests
import logging
import random
import json

class Response():
    def __init__(self, group, analyzer):
        self.responseText = ''
        self.responseType = 'text'
        self.group = group
        self.analyzer = analyzer

    def send(self):
        url = 'https://api.groupme.com/v3/bots/post'
        if self.responseText:
            body = {}
            if self.responseType == 'mention':
                body = {'bot_id': self.group.gmBotId,
                        'text': self.responseText,
                        'attachments': [
                            {"type": "mentions",
                            "loci": self.get_message_loci(),
                            "user_ids": self.group.memberIds}
                        ]
                    }
            elif self.responseType == 'text':
                body = {
                    'bot_id': self.group.gmBotId,
                    'text': self.responseText
                }
            resp = requests.post(url, json=body)
            if resp.status_code == 202:
                logging.warn("Message Posted")
            else:
                logging.warn("Message failed to post: "+ str(resp.status_code))
    
    def help(self):
        self.responseText = """
        The following commands are supported: \n

        @all - tag all users in the GroupMe \n

        --randomhouses <gamename> <userlist:comma-delimited> \n
        ex: --randomhouses 3p scott,steve,maulik \n
        supported games: RTKL, NKFD, RITS, SITN, 3p \n
        If the game size does not match the number of groupme members then you must specify the members to include \n
        Don't include spaces in the message except between parameters \n
        Player names should be separated by commas\n
        """

    def mentionAll(self):
        start_text, end_text = self.get_surrounding_text()
        mentions = self.create_mention_text()
        self.responseText = start_text + ' '+ mentions + ' '+ end_text
        self.responseType = 'mention'

    def randomHouseDraw(self):
        command = self.analyzer.messageText.split(" ")
        houseList = self.getHouseList(command[1])
        random.shuffle(houseList)
        names = self.group.memberNames.copy()
        if len(command) > 2:
            names = self.getMemberNamesFromInput(command[2])
        random.shuffle(names)
        t = 'House Assignment: \n'
        if len(names) > 0 and len(houseList) == len(names):
            for name in names:
                t += name + ': ' + houseList[names.index(name)] + '\n'
            self.responseText = t
        else:
            logging.warn("Game requested does not match user list")
            logging.warn('Names: {}'.format(names))
            logging.warn('HouseList: {}'.format(houseList))
            self.responseText = "Invalid input provided"

    def getMemberNamesFromInput(self, players):
        text = players.lower()
        text.split(",")
        names = []
        if isinstance(text, str): #used for single person group
            text = [text]
        for p in text:
            for member in self.group.memberNames:
                logging.warn('P: {}, Member: {}'.format(p, member))
                if p in member.lower():
                    names.append(member)
        return names

    def getHouseList(self, game):
        text = game.lower()
        houseList = []
        if 'rtkl' in text:
            houseList = ['Lannister', 'Greyjoy', 'Tyrell', 'Stark', 'Martell']
        elif 'nkfd' in text:
            houseList = ['Lannister', 'Baratheon', 'Tyrell', 'Stark', 'Martell']
        elif 'rits' in text:
            houseList = ['Lannister', 'Baratheon', 'Tyrell', 'Martell']
        elif 'sitn' in text:
            houseList = ['Lannister', 'Baratheon', 'GreyJoy', 'Stark']
        elif '3p' in text:
            houseList = ['Lannister', 'Baratheon', 'Stark']
        elif 'test' in text:
            houseList = ['TestHouseFor1User']
        return houseList

    def get_surrounding_text(self):
        l = self.analyzer.messageText.lower()
        start_index = l.find("@all")
        start_text = ""
        if start_index > 0:
            start_text = self.analyzer.messageText[0:start_index]
        end_index = start_index + 4
        end_text = self.analyzer.messageText[end_index+1:len(self.analyzer.messageText)]
        return start_text, end_text

    def create_mention_text(self):
        msg = ""
        for name in self.group.memberNicknames:
            msg += "@"+name+", "
        msg = msg[0:-2]
        return msg

    def get_message_loci(self):
        loci = []
        for name in self.group.memberNicknames:
            start = self.responseText.find(name)
            if start:
                end = start + len(name)
                #logging.warning("Loci are: " + start +" " +end])
                loci.append([start, end])
        return loci