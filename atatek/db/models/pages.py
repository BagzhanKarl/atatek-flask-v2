from datetime import datetime
from atatek.db import db

class Pages(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    juz = db.Column(db.String(100), nullable=False)
    breed1 = db.Column(db.String(100), nullable=False)
    breed2 = db.Column(db.String(100), nullable=False)
    breed3 = db.Column(db.String(100), nullable=False)
    subdomain = db.Column(db.String(100), nullable=False)

    tree_id = db.Column(db.Integer, db.ForeignKey('main_tree.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class PopularPeople(db.Model):
    __tablename__ = 'popular_people'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.String(100), nullable=True)
    page = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Moderators(db.Model):
    __tablename__ = 'moderators'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    page = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)