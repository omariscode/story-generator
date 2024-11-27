import firebase_admin
from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hhahaha'

CORS(app)

cred = credentials.Certificate("./story.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

from app import routes