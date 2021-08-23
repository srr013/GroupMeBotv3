from app import db
import datetime
from sqlalchemy.orm import relationship

class Bot(db.Model):
    __tablename__ = 'bots'
    id = db.Column(db.String(), primary_key=True)
    botName = db.Column(db.String())
    callbackUrl = db.Column(db.String())
    avatarUrl = db.Column(db.String())
    createdDate = db.Column(db.Date)
    group = relationship("Group", back_populates="bot")

    def __init__(self, botId, botName, callbackUrl, avatarUrl):
        self.id = botId
        self.botName = botName
        self.callbackUrl = callbackUrl
        self.avatarUrl = avatarUrl
        self.createdDate = datetime.datetime.today().strftime("%Y-%m-%d")


    def __repr__(self):
        return '<id {}>'.format(self.id)

    def deserialize(self):
        bot = {
            "Bot Name": self.botName,
            "ID": self.id,
            "Callback Url":self.callbackUrl,
            "Avatar Url": self.avatarUrl,
            "Created Date": self.createdDate.strftime("%Y-%m-%d")
        }
        return bot
