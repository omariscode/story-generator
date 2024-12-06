import os
import firebase_admin
from flask import Flask
from flask_cors import CORS
from huggingface_hub import InferenceClient
from firebase_admin import credentials, firestore

IMAGE_DIR = "static/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hhahaha'

CORS(app)

cred = credentials.Certificate("./story.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

client = InferenceClient("black-forest-labs/FLUX.1-dev", token="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")

from app import routes
