import models.MessageTypes._DefaultMessageType as Default
import random
import logging

class RandomHouseDraw(Default.DefaultMessageType):
    def __init__(self):
        super().__init__()
        self.qualifyingText = ['randomhouses']
        self.responseType = 'text'
    
    def constructResponseText(self, payload, response):
        responseText = ''
        inboundMessage = payload.get('text')
        command = inboundMessage.split(" ")
        houseList = self.getHouseList(command[1])
        random.shuffle(houseList)
        names = response.group.memberNames.copy()
        if len(command) > 2:
            names = command[2].split(",")
        random.shuffle(names)
        t = 'House Assignment: \n'
        if len(names) > 0 and len(houseList) == len(names):
            for name in names:
                t += name + ': ' + houseList[names.index(name)] + '\n'
            responseText = t
        else:
            logging.warn("Game requested does not match user list")
            logging.warn('Names: {}'.format(names))
            logging.warn('HouseList: {}'.format(houseList))
            responseText = "Invalid input provided"
        return responseText



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