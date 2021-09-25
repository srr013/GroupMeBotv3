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
SQLALCHEMY_DATABASE_URI = clean('SQLALCHEMY_DATABASE_URI')
TEST_GROUPS = clean('TEST_GROUPS')
S3_REGION = clean('S3_REGION')
AWS_S3_USER_KEY = clean('AWS_S3_USER_KEY')
AWS_S3_USER_SECRET = clean('AWS_S3_USER_SECRET')
BUCKET_NAME = 'insultbot-memes'
UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'json'}
DEFAULT_IMAGE_NAME = 'notFoundYouJackass.jpg'