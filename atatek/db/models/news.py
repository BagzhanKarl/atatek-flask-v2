from datetime import datetime
from atatek.db import db

class NewsSettings(db.Model):
    __tablename__ = 'news_settings'

    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)
    logo = db.Column(db.String(200), nullable=False)
    newsletter_bg = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    poster = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    clicks = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class Coments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sender = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

