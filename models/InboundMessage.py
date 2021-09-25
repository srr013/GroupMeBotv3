from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
import datetime
import logging
import services.config as config

class InboundMessage(db.Model):
    __tablename__ = 'inboundMessages'
    id = db.Column(db.Integer(),primary_key=True)
    messageText = db.Column(db.String())
    createdDateTime = db.Column(db.DateTime())
    groupId = db.Column(db.String(), ForeignKey('groups.groupId'))
    sendingUser = db.Column(db.String())
    sendingUserType = db.Column(db.String())
    outboundMessageId = db.Column(db.Integer(), ForeignKey('outboundMessages.id'))
    outboundMessage = relationship("OutboundMessage", back_populates="inboundMessage")
    group = relationship("Group", back_populates='inboundMessage')

    def __init__(self, payload):
        self.messageText = payload.get("text")
        self.createdDateTime = datetime.datetime.utcfromtimestamp(payload.get("created_at")).strftime("%Y-%m-%d %H:%M:%S")
        self.groupId = payload.get("group_id")
        self.sendingUser = payload.get("sender_id")
        self.sendingUserType = payload.get("sender_type")
        self.sourceGuid = payload.get("source_guid")
        self.outboundMessageId = None

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def validateGroupmePost(self, allowBot=False):
        isValid = False
        if allowBot:
            if self.sendingUserType != "system"\
                and self.messageText('text') \
                    and self.groupId('group_id') \
                        and self.sourceGuid:
                isValid = True
        else:
            if self.sendingUserType not in ["bot", "system"] \
                and self.sendingUserType \
                    and self.groupId \
                        and self.messageText  \
                            and self.sourceGuid:
                isValid = True
        return isValid

    def isBotOrSystemMessage(self, payload):
        if payload.get('sender_type') in ["bot", "system"]:
            return True
        return False

    def deserialize(self):
        data = {
            "Group": self.groupId,
            "ID": self.id,
            "Created Date & Time": self.createdDateTime.strftime("%Y-%m-%d"),
            "Message Text": self.messageText,
            "Triggering User": self.sendingUser,
            "Triggering User Type": self.sendingUserType
        }
        return data


