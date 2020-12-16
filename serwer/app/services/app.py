from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# should be taken care of when deployed publicly
