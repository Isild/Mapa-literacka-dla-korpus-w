from app.controllers import init_routes
from flask_cors import CORS
from app.services.app import app as flask_app
from app.services.db import init_db


def init_app():
    CORS(flask_app)
    init_db()
    init_routes()
