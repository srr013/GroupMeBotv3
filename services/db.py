# import os
# import psycopg2
# import logging



# """
# table name: groupme_yahoo
#       column_name      |     data_type
# -----------------------+-------------------
#  message_num           | integer
#  message_limit         | integer
#  num_past_transactions | integer
#  league_data           | json
#  status                | integer
#  messaging_status      | integer
#  bot_id                | character varying
#  members               | json
#  groupme_group_id      | integer
#  index                 | integer
#  messages              | character varying


# table name: userGroup
# CREATE TABLE userGroup(
#     id TEXT,
#     botId TEXT,
#     messagingServiceStatus BOOLEAN,
#     counter_lowerBound INTEGER,
#     counter_upperBound INTEGER,
#     counter_currentThreshold INTEGER,
#     counter_current INTEGER,
#     messageTypes TEXT ARRAY
# );

# table name: users
# CREATE TABLE users(
#     id SERIAL PRIMARY KEY,
#     email TEXT UNIQUE,
#     firstName TEXT,
#     lastName TEXT,
#     userGroups INTEGER ARRAY
# );

# application_data
#     column_name    | data_type
# -------------------+-----------
#  monitoring_status | boolean
#  messaging_status  | boolean

# triggers TODO: rename
#         column_name         |        data_type
# ----------------------------+--------------------------
#  i                          | integer
#  type                       | character varying
#  days                       | ARRAY
#  periods                    | ARRAY
#  status                     | ARRAY
#  group_id                   | integer

# """

# def initialize_connection():
#     if os.environ.get('DATABASE_URL'):
#         DATABASE_URL = os.environ['DATABASE_URL']
#         conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#         return conn
#     return False

# def execute_table_action(query, values = ()):
#     conn = initialize_connection()
#     if conn:
#         cursor = conn.cursor()
#         try:
#             if not values:
#                 cursor.execute(query)
#             else:
#                 cursor.execute(query, values)
#         except Exception as e:
#             logging.warn("Exception occurred writing to DB: "+ e)
#         conn.commit()
#         conn.close()

# def fetch_all(query, values = ()):
# 	conn = initialize_connection()
# 	cursor = conn.cursor()
# 	if not values:
# 		cursor.execute(query)
# 	else:
# 		cursor.execute(query, values)
# 	l = cursor.fetchall()
# 	conn.commit()
# 	conn.close()
# 	return l

# def fetch_one(query, values = ()):
# 	conn = initialize_connection()
# 	cursor = conn.cursor()
# 	if not values:
# 		cursor.execute(query)
# 	else:
# 		cursor.execute(query, values)
# 	l = cursor.fetchone()
# 	conn.commit()
# 	conn.close()
# 	return l



# triggers =  """CREATE TABLE triggers(i SERIAL PRIMARY KEY, type VARCHAR(50),
# days VARCHAR[], periods VARCHAR[], 
# status VARCHAR[], group_id INTEGER REFERENCES groupme_yahoo(index));
# """

# create_table = """
# CREATE TABLE groupme_yahoo(message_num, message_limit, 
# num_past_transactions, status, messaging_status, bot_id, members, groupme_group_id, index);
# """
# app_status = """CREATE TABLE application_data(monitoring_status BOOLEAN, messaging_status BOOLEAN);"""

# drop_table = """
# DROP TABLE 
# """
# insert_into = """
# INSERT INTO groupme_yahoo(group_id, message_num, message_limit, 
# num_past_transactions, league_data, status, messaging_status, bot_id) 
# VALUES
#     ();
# """
# serial = """ALTER TABLE groupme_yahoo ADD COLUMN index SERIAL PRIMARY KEY;"""

# select = """
# SELECT * FROM groupme_yahoo
# """
# add = """
# ALTER TABLE groupme_yahoo ADD COLUMN status INTEGER, 
# bot_status INTEGER, prd_bot VARCHAR(100), test_bot VARCHAR(200);
# """
# #works from CLI, not debug

# update = """
# UPDATE groupme_yahoo SET status, bot_status, WHERE group_id=1;
# """
