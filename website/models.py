from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Tasks(db.Model):
    __tablename__ = 'tasks'
    serial = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return f"{self.serial}-{self.title}"


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    tasks = db.relationship(Tasks)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password
