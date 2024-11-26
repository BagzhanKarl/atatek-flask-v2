from datetime import datetime
from atatek.db import db

class Tree(db.Model):
    __tablename__ = 'main_tree'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth = db.Column(db.Integer, nullable=True)
    death = db.Column(db.Integer, nullable=True)

    parent_id = db.Column(db.Integer, db.ForeignKey('main_tree.id'))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    status = db.Column(db.Boolean, nullable=True)
    item_id = db.Column(db.Integer, nullable=True)

    parent = db.relationship('Tree', remote_side=[id], foreign_keys=[parent_id], backref='children')


class TreeInfo(db.Model):
    __tablename__ = 'tree_info'

    id = db.Column(db.Integer, primary_key=True)
    tree_id = db.Column(db.Integer, db.ForeignKey('main_tree.id'))
    info = db.Column(db.Text, nullable=False)
    tree_icon = db.Column(db.String(100), nullable=True)
    tree_full_icon = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), default=1)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), default=1)