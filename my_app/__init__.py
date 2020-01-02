import os
import mysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_marshmallow import Marshmallow
from my_app.settings import app_cfg, db_config
from my_app.check_dir_tree import check_dir_tree
from base64 import b64encode
from my_app.my_secrets import passwords

application = app = Flask(__name__)

# Assign App Config Variables / Create a random token for Flask Session
token = os.urandom(64)
token = b64encode(token).decode('utf-8')
app.config['SECRET_KEY'] = token
app.config['UPLOADED_FILES_DEST'] = os.path.join(app_cfg['HOME'], app_cfg['MOUNT_POINT'],
                                                 app_cfg['MY_APP_DIR'], app_cfg['UPDATES_SUB_DIR'])


# Get the Passwords and Keys
print()
print("\tI have a DB Password: ", my_secrets.passwords["DB_PASSWORD"])
print("\tI have an SmartSheet API Key: ", my_secrets.passwords["SS_TOKEN"])
print("\tI have an Flask Secret Key: ", app.config['SECRET_KEY'])
print("\tRuntime Environment is:", app_cfg['RUNTIME_ENV'])
print()

#
# Check and Build Directory Tree as needed
#
check_dir_tree()

#
# database connection settings
#

# # Create connection to MySQL
#
# ADD 'allow_local_infile' here  AND
# In the my.ini file ADD
# [mysqld]
# local_infile=1
my_mysql_options = '?charset=utf8&allow_local_infile=true'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' +\
                                            db_config['USER'] +\
                                        ':'+db_config['PASSWORD'] +\
                                        '@'+db_config['HOST']+':3306'

print('\t\tDatabase Connection String:', app.config['SQLALCHEMY_DATABASE_URI'])

# Create an engine and connect to the engine / server
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])  # connect to server

# Create DEFAULT Database from the Settings file
engine.execute("CREATE SCHEMA IF NOT EXISTS `" + db_config['DATABASE'] + "`;")  # create db
engine.execute("USE " + db_config['DATABASE'] + ";")  # select new db

# Update the URI and attach the schema for multiple URI databases
# app.config['SQLALCHEMY_BINDS']= {
#     'dev':        'mysqldb://localhost/users',
#     'prod':       'sqlite:////path/to/appmeta.db'
# }
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'] + "/" + db_config['DATABASE'] + \
                                        my_mysql_options
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
print('SQLALCHEMY_DATABASE_URI is:', app.config['SQLALCHEMY_DATABASE_URI'])


#
# # Create db for SQL Alchemy
db = SQLAlchemy(app)

#
# # Create ma for Marshmallow
ma = Marshmallow(app)


# Are we connected if so How & Where ?
db_host = []
db_port = []
db_user = []
db_status = (db.engine.execute("SHOW VARIABLES WHERE Variable_name = 'port'"))
for x in db_status:
    db_port = x.values()

db_status = (db.engine.execute("SHOW VARIABLES WHERE Variable_name = 'hostname'"))
for x in db_status:
    db_host = x.values()

db_status = (db.engine.execute('SELECT USER()'))
for x in db_status:
    db_user = x.values()

print('\tYou are connected to MySQL Host '+db_host[1]+' on Port '+db_port[1]+' as '+db_user[0])


from my_app import views
from my_app import models
