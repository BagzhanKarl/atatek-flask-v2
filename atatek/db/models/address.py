from atatek.db import db

class Places(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    osm = db.Column(db.String(250), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    display_name = db.Column(db.String(250), nullable=False)