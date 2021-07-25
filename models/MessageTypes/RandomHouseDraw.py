import models.MessageTypes._DefaultMessageType as Default
import random
import logging

class RandomHouseDraw(Default.DefaultMessageType):
    def __init__(self, group):
        super().__init__(group)
        self.qualifyingText = ['randomhouses']
        self.responseType = 'text'
        self.helpText = """
--randomhouses <gamename> <userlist:comma-delimited>: Supported games: RTKL, NKFD, RITS, SITN, 3p. If the game size does not match the number of groupme members then you must specify the members to include. Don't include spaces in the message except between parameters. Player names should be separated by commas. ex: --randomhouses 3p paul,ringo,john
"""
    
    def constructResponseText(self, payload, response):
        responseText = ''
        inboundMessage = payload.get('text')
        command = inboundMessage.split(" ")
        houseList = self.getHouseList(command[1])
        random.shuffle(houseList)
        names = response.groupMeGroup.memberNames.copy()
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