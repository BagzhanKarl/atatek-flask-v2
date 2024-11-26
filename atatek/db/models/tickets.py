from datetime import datetime
from atatek.db import db

class Tickets(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(15))

    is_active = db.Column(db.Boolean, default=True)
    is_cancelled = db.Column(db.Boolean, default=False)
    is_confirmed = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class EditTicket(db.Model):
    __tablename__ = 'edit_requests'
    id = db.Column(db.Integer, primary_key=True)
    ticket = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    tree = db.Column(db.Integer, db.ForeignKey('main_tree.id'))
    name = db.Column(db.String(50))
    birth = db.Column(db.Integer)
    death = db.Column(db.Integer)

    biography = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class AddTicket(db.Model):
    __tablename__ = 'add_requests'
    id = db.Column(db.Integer, primary_key=True)
    ticket = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    parent = db.Column(db.Integer, db.ForeignKey('main_tree.id'))
    name = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
