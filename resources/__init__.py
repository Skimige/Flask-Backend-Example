import os
from configparser import ConfigParser

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

config = ConfigParser()
config.read(os.path.join('config.ini'))


app = Flask(__name__)
# SQLAlchemy Config
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLAlchemy', 'DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.getboolean('SQLAlchemy', 'TRACK_MODIFICATIONS')
# JWT Config
app.config['JWT_SECRET_KEY'] = bytes(config.get('JWT', 'SECRET_KEY'), 'utf-8')
app.config['JWT_BLACKLIST_ENABLED'] = config.getboolean('JWT', 'BLACKLIST_ENABLED')
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']  # ['access', 'refresh']
db = SQLAlchemy(app)
api = Api(app)
# migrate = Migrate(app, db)
jwt = JWTManager(app)
