import os
import logging

def clean(name):
    var = os.environ.get(name, None)
    if var:
        return var
    else:
        logging.error(f"Env variable {name} not found")

GROUPME_ACCESS_TOKEN = clean('GM_ACCESS_TOKEN')
SECRET = clean('SECRET_KEY')
GM_BOT_ID_TEST = clean('GM_BOT_ID_TEST')
DATABASE_URL = clean('DATABASE_URL')
SQLALCHEMY_DATABASE_URI = clean('SQLALCHEMY_DATABASE_URI')