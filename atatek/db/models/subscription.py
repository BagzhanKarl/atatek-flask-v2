from atatek.db import db

class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    addchild = db.Column(db.Integer, nullable=False, default=False)
    addinfo = db.Column(db.Integer, nullable=False, default=False)
    start_date = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)  # Дата начала
    end_date = db.Column(db.DateTime, nullable=False)  # Дата окончания

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'start_date' not in kwargs:  # Если start_date не задан, берем текущую дату
            self.start_date = datetime.utcnow()
        self.end_date = self.start_date + timedelta(days=30)  # Устанавливаем дату окончания через месяц
