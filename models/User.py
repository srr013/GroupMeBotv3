
# from app import db
# import datetime
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.schema import ForeignKey
# from sqlalchemy.dialects.postgresql import ARRAY


# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String())
#     firstName = db.Column(db.String())
#     lastName = db.Column(db.String())
#     createdDateTime = db.Column(db.DateTime)
#     # groups = db.Column(db.Integer(), ForeignKey('groups.id'))
#     # group = relationship("Group", back_populates="user")

#     def __init__(self, body):
#         self.id = ''
#         self.email = ''
#         self.firstName = ''
#         self.lastName = ''
#         # self.photoUrl
#         self.groups = []
#         self.createdDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


#     def deserialize(self):
#         data = {
#             "ID": self.id,
#             "Name": f"{self.lastName}, {self.firstName}",
#             "Email": self.email,
#             "Group List": self.groups,
#             "Created Date & Time": self.createdDateTime.strftime("%Y-%m-%d")
#         }
#         return data
#     #     query = 'SELECT * FROM users WHERE email=%s'
#     #     values = (email,)
#     #     data = db.fetch_one(query, values)
#     #     if data:
#     #         self.id = data[0]
#     #         self.email = data[1]
#     #         self.firstName = data[2]
#     #         self.lastName = data[3]
#     #         self.userGroups = data[4]
#     #         logging.warn("User deserialized")
#     #         return True
#     #     else:
#     #         logging.error(f"No user found: {self.id}")
#     #         return False

#     # def serialize(self):
#     #     query = """
#     #     UPDATE users SET
#     #     email = %s,
#     #     firstName = %s,
#     #     lastName = %s,
#     #     userGroups = %s
#     #     WHERE id = %s
#     #     """
#     #     values = (
#     #         self.email,
#     #         self.firstName,
#     #         self.lastName,
#     #         self.userGroups,
#     #         self.id)

#     #     db.execute_table_action(query, values)
#     #     logging.warn("Group serialized to DB")

#     # def createUser(self, data):
#     #     logging.warn(f"Creating user from email: {data['email']}")
#     #     query = """
#     #     INSERT INTO users(
#     #     email,
#     #     firstName,
#     #     lastName,
#     #     userGroups)
#     #     VALUES (%s,%s,%s,%s)
#     #     RETURNING id;
#     #     """
#     #     values = ( 
#     #         data['email'],
#     #         data['firstName'],
#     #         data['lastName'],
#     #         [])
#     #     self.id = db.fetch_one(query, values)[0]
#     #     self.email = data['email']
#     #     self.firstName = data['firstName']
#     #     self.lastName = data['lastName']