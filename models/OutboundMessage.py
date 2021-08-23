from app import db
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

class OutboundMessage(db.Model):
    __tablename__ = 'outboundMessages'
    id = db.Column(db.Integer, primary_key=True)
    messageText = db.Column(db.String())
    createdDateTime = db.Column(db.DateTime)
    group_id = db.Column(db.Integer(), ForeignKey('groups.id'))
    triggeringUser = db.Column(db.String())
    inboundMessage = relationship("InboundMessage", back_populates="outboundMessage")

    def __init__(self, response):
        self.messageText = response.responseText
        self.createdDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.groupMeGroup = response.groupMeGroup
        self.group_id = response.groupMeGroup.group.id
        self.triggeringUser = response.inboundMessagePayload.get("sender_id")

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def deserialize(self):
        data = {
            "Group": self.groupMeGroup.group.id,
            "ID": self.id,
            "Created Date & Time": self.createdDateTime.strftime("%Y-%m-%d"),
            "Message Text": self.messageText,
            "Triggering User": self.triggeringUser
        }
        return data