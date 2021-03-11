from flask_drama import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    drama_id = db.Column(db.Integer, db.ForeignKey('dramas.id'))
    star = db.Column(db.Integer)
    review = db.Column(db.String(200))

    def __init__(self, drama_id=None, star=None, review=None):
        self.drama_id = drama_id
        self.star = star
        self.review = review
