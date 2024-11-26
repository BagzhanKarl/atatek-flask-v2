from datetime import datetime

from atatek.db import db

class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    add_child = db.Column(db.Integer, nullable=False, default=False)
    add_info = db.Column(db.Integer, nullable=False, default=False)
    price = db.Column(db.Float, nullable=False, default=0.00)
    personal_page = db.Column(db.Boolean, nullable=False, default=True)
    all_pages = db.Column(db.Boolean, nullable=False, default=False)
    family_person_count = db.Column(db.Integer, nullable=False, default=0)


    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    def __repr__(self):
        return f'<Role {self.id}>'
