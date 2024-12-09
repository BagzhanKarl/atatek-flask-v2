from functools import wraps
from flask import Flask
from atatek import endpoints
from atatek.db import db
from atatek.endpoints import *
from atatek.utils import verify_jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://atatek:atatek@localhost/atatek'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TIMEZONE'] = 'UTC'  # или 'Asia/Almaty'
app.secret_key = 'atatek'
db.init_app(app)


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(main)
app.register_blueprint(pages)
app.register_blueprint(admin)

app.register_blueprint(api, url_prefix='/api')

app.register_blueprint(install)


@app.route('/release')
def release():
    return render_template('release.html')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()