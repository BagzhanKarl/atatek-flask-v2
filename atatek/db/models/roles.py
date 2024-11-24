from datetime import datetime

from atatek.db import db

class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    add_child = db.Column(db.Integer, nullable=False, default=False)
    add_info = db.Column(db.Integer, nullable=False, default=False)
    price = db.Column(db.Float, nullable=False, default=0.00)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Role {self.id}>'
