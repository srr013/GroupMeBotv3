


DB Migrations
To initialize a migration: py manage.py db init
To migrate: py manage.py db migrate
To upgrade (after a change): py manage.py db upgrade
To update the DB on heroku:  heroku run python manage.py db upgrade
    -make sure the SQLALCHEMY_DATABASE_URI app.config value is set, not just env.

Always migrate then upgrade