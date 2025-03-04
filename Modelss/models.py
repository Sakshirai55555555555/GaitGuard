# models/models.py
from .database import db

class User(db.Model):
    __tablename__ = 'users'  # Make sure the table name fits your preference
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    security_question = db.Column(db.String(150), nullable=False)
    security_answer = db.Column(db.String(150), nullable=False)
