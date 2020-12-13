import requests
import logging
import random

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
                
    def mentionAll(self):
        start_text, end_text = self.get_surrounding_text()
        mentions = self.create_mention_text()
        self.responseText = start_text + ' '+ mentions + ' '+ end_text
        self.responseType = 'mention'

    def randomHouseDraw(self):
        houseList = ['Lannister']#, 'Baratheon', 'Tyrell', 'Stark', 'Martell']
        random.shuffle(houseList)
        names = self.group.memberNicknames.copy()
        random.shuffle(names)
        t = 'House Assignment: \n'
        if len(houseList) == len(names):
            for name in names:
                t += name + ': ' + houseList[names.index(name)] + '\n'
            self.responseText = t
        else:
            logging.warn("Game requested does not match user list")


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