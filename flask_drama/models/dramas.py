from flask_drama import db


class Drama(db.Model):
    __tablename__ = 'dramas'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    actor = db.Column(db.String(100))
    mean = db.Column(db.Float)
    rate = db.Column(db.Float)
    posts = db.relationship('Post', backref='drama', lazy='dynamic')

    def __init__(self, title=None, actor=None, mean=None, rate=None):
        self.title = title
        self.actor = actor
        self.mean = mean
        self.rate = rate
