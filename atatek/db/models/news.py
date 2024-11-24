from datetime import datetime
from atatek.db import db

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    poster = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    clicks = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Coments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sender = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

