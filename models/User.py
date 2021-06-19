import requests
import json
import logging
import os
import services.db as db


class User():
    def __init__(self, body):
        self.id = ''
        self.email = ''
        self.firstName = ''
        self.lastName = ''
        # self.photoUrl
        self.userGroups = []
        if not self.deserialize(body['email']):
            self.createUser(body)

    def deserialize(self, email):
        query = 'SELECT * FROM users WHERE email=%s'
        values = (email,)
        data = db.fetch_one(query, values)
        if data:
            self.id = data[0]
            self.email = data[1]
            self.firstName = data[2]
            self.lastName = data[3]
            self.userGroups = data[4]
            logging.warn("User deserialized")
            return True
        else:
            logging.error(f"No user found: {self.id}")
            return False

    def serialize(self):
        query = """
        UPDATE users SET
        email = %s,
        firstName = %s,
        lastName = %s,
        userGroups = %s
        WHERE id = %s
        """
        values = (
            self.email,
            self.firstName,
            self.lastName,
            self.userGroups,
            self.id)

        db.execute_table_action(query, values)
        logging.warn("Group serialized to DB")

    def createUser(self, data):
        logging.warn(f"Creating user from email: {data['email']}")
        query = """
        INSERT INTO users(
        email,
        firstName,
        lastName,
        userGroups)
        VALUES (%s,%s,%s,%s)
        RETURNING id;
        """
        values = ( 
            data['email'],
            data['firstName'],
            data['lastName'],
            [])
        self.id = db.fetch_one(query, values)[0]
        self.email = data['email']
        self.firstName = data['firstName']
        self.lastName = data['lastName']