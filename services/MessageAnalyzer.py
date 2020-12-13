
class MessageAnalyzer():
    def __init__(self, payload):
        self.payload = payload
        self.messageText = payload.get("text")
        self.isGroupmePost = self.validateGroupmePost()

    def validateGroupmePost(self, allowBot=False):
        isValid = False
        if allowBot:
            if self.payload.get('sender_type') \
                and self.messageText \
                    and self.payload.get('group_id') \
                        and self.payload.get("source_guid"):
                isValid = True
        else:
            if self.payload.get('sender_type') != "bot" \
                and self.payload.get('sender_type') \
                    and self.payload.get('group_id') \
                        and self.messageText \
                            and self.payload.get("source_guid"):
                isValid = True
        return isValid

    def mentionAllMembers(self):
        if "@all" in self.messageText.lower():
            return True
        return False

    def randomHouseSelector(self):
        if "--randomhouses" in self.messageText.lower():
            return True
        return False
