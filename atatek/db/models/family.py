from datetime import datetime
from atatek.db import db


class Family(db.Model):
    __tablename__ = 'family'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    birthday = db.Column(db.String(20), nullable=True)
    death = db.Column(db.String(20), nullable=True)
    alive = db.Column(db.Boolean, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    pids = db.Column(db.String(50), nullable=True)  # Parent
    fid = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=True)  # Father
    mid = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=True)  # Mother
    bid = db.Column(db.String(20),  nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Определение отношений
    father = db.relationship('Family', remote_side=[id], foreign_keys=[fid], backref='father_children')
    mother = db.relationship('Family', remote_side=[id], foreign_keys=[mid], backref='mother_children')
