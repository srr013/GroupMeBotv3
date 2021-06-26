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
DATABASE_URL = clean('DATABASE_URL')
SQLALCHEMY_DATABASE_URI = clean('SQLALCHEMY_DATABASE_URI')
TEST_GROUPS = clean('TEST_GROUPS')