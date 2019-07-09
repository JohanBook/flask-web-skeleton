"""
This module contains data tables and related methods.
"""

from datetime import datetime

from flask import current_app, url_for
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from jedi import db, login_manger


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    Table for a user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    confirmed_email = db.Column(db.Boolean(), nullable=False, default=False)
    image_file = db.Column(
        db.String(20), nullable=False, default="default.png"
    )
    password = db.Column(db.String(60), nullable=False)
    credit = db.Column(db.Integer, nullable=False, default=100)
    purchases = db.relationship("Purchase", backref="owner", lazy=True)

    # privilege = db.Column(db.Integer, nullable=False, default=0)

    def check_credit(self, amount):
        return self.credit >= amount

    def get_reset_token(self, expires_sec=1800):
        serializer = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return serializer.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = serializer.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def withdraw_credit(self, amount):
        self.credit = self.credit - amount
        db.session.commit()

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Purchase(db.Model):
    """
    Table for purchases
    """

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Purchase('{self.owner}', '{self.address}', '{self.date}')"
