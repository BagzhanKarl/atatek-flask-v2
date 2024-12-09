from atatek.db import db
from datetime import datetime
class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    addchild = db.Column(db.Integer, nullable=False, default=False)
    addinfo = db.Column(db.Integer, nullable=False, default=False)
    personal = db.Column(db.Boolean, nullable=False)
    allpage = db.Column(db.Boolean, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    days = db.Column(db.Integer, nullable=False)
    family_person_count = db.Column(db.Integer, nullable=False, default=0)

    is_active = db.Column(db.Boolean, nullable=False, default=True)