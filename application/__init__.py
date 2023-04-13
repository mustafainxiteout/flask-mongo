#Importing necessary modules
from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restx import Api
from flask_cors import CORS
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_jwt_extended import JWTManager

#Initializing the Flask app and configuring it using the Config class
app=Flask(__name__)
app.config.from_object(Config)

#Initializing the MongoEngine object and binding it to the Flask app instance
db=MongoEngine()
db.init_app(app)

mail = Mail(app)

# configure URLSafeTimedSerializer
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

#Allowing cross-origin resource sharing (CORS)
cors = CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})

#Initializing the Flask-RESTX API object and binding it to the Flask app instance
api=Api()
api.init_app(app)

jwt = JWTManager(app)

#Importing the routes module where the app routes are defined
from application import routes 