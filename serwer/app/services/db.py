from flask_sqlalchemy import SQLAlchemy
from app.services.app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../database.db'
db = SQLAlchemy(app)

# This line breaks flake8 lint and needs to be no-linted. Maybe it is possible
# to write it diffrently, but even the official example from SQLAlchemy needs
# to be no-linted.
from app.models.literary_map import LiteraryMap  # noqa: F401, E402

db.create_all()
