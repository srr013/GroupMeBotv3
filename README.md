


DB Migrations
To initialize a migration: py manage.py db init
To migrate: py manage.py db migrate
To upgrade (after a change): py manage.py db upgrade
To update the DB on heroku:  heroku run python manage.py db upgrade
    -make sure the SQLALCHEMY_DATABASE_URI app.config value is set, not just env.
    -If you're adding new columns the migration works without dropping
    -If you're changing columns?

Always migrate then upgrade

If you need to change a data type then truncate tables including the alembic_version table (non-prd). Then db init, etc.

Managing a local and PRD DB:
Need to manage each individually. Binds parameter doesn't seem applicable. don't gitignore the migrations folder. May need to truncate the remote DB alembic_version table before running manage.py upgrade.

when migrating/upgrading it needs to be done to all servers. Otherwise you need to drop and re-create locally then remotely?

Run specific database changes directly on the DB table/column to allow a migration/upgrade without dropping the table. e.g.
ALTER TABLE groups ADD CONSTRAINT constraint_name UNIQUE ("groupId");

Or SSH into the Heroku host and make updates there. Allows you to perform the init and migrate + upgrade properly if CLI doesn't work.
heroku ps:exec to ssh