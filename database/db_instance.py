from flask_sqlalchemy import SQLAlchemy
from server.server import app

db = SQLAlchemy(app)