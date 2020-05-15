import datetime as dt
from music_blog.extensions import db, bcrypt


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Binary(128), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=dt.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=dt.datetime.utcnow)
    bio = db.Column(db.String(300), nullable=True)
    image = db.Column(db.String(120), nullable=True)
    token: str = ''

    def __init__(self, username, email, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if(password):
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)
