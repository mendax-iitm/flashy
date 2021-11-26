from enum import unique
from sqlalchemy.orm import backref
from .database import db
from flask_security import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    deck = db.relationship(
        "Deck", backref='user', lazy=True)
    
    def __init__(self, username, active=0):
        self.username=username
        self.active=active 

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


    def get_id(self):
        return self.id


class Deck(db.Model):
    __tablename__ = "deck"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    review_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    deck_score = db.Column(db.Integer, default=0)
    card = db.relationship("Card", backref='deck')


class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    front = db.Column(db.String)
    back = db.Column(db.String)
    deck_id = db.Column(db.Integer, db.ForeignKey(
        'deck.id'), primary_key=True, nullable=False)
    review = db.Column(db.Integer)
    


# class ArticleAuthors(db.Model):
#     __tablename__ = "article_authors"
#     user_id = db.Column(
#         db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False
#     )
#     article_id = db.Column(
#         db.Integer,
#         db.ForeignKey("article.article_id"),
#         primary_key=True,
#         nullable=False,
#     )
