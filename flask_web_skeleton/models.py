"""
This module contains data tables and related methods.
"""
from datetime import datetime
from hashlib import md5
from secrets import token_hex
# from hmac import compare_digest

from flask import current_app
from flask_login import UserMixin
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask_web_skeleton import bcrypt, db, login_manger

INITIAL_CREDIT = 100
PASSWORD_BYTES = 32


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

    # Info
    image_file = db.Column(
        db.String(20), nullable=False, default=None#"default.png"
    )

    # Authentication
    hashed_password = db.Column(db.String(2 * PASSWORD_BYTES), nullable=False)
    salt = db.Column(db.String(2 * PASSWORD_BYTES), nullable=False)
    reset_token = db.Column(db.String(16), default="")

    # Economic
    credit = db.Column(db.Integer, nullable=False, default=INITIAL_CREDIT)
    purchases = db.relationship("Purchase", backref="owner", lazy=True)

    # privilege = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self._set_password(password)

    def _set_password(self, password):
        self.salt = token_hex(PASSWORD_BYTES)
        self.hashed_password = bcrypt.generate_password_hash(
            self.salt + password
        )
        db.session.commit()

    def set_password(self, password):
        """
        Generate new salt and store password hash in database.
        """
        if self.check_password(password):
            raise ValueError("Password must differ from previous password")
        self._set_password(password)

    def check_password(self, password):
        """
        Check entered password against stored hash.

        Returns:
            bool: Password match.
        """
        return bcrypt.check_password_hash(
            self.hashed_password, self.salt + password
        )

    def login(self):
        self.reset_token = None

    def check_credit(self, amount):
        return self.credit >= amount

    def withdraw_credit(self, amount):
        self.credit = self.credit - amount
        db.session.commit()

    def get_token(self, content=None, expires_in=15 * 60):
        serializer = Serializer(current_app.config["SECRET_KEY"], expires_in)
        return serializer.dumps(
            {"user_id": self.id, "content": content}
        ).decode("utf-8")

    def password_reset_request(self):
        self.reset_token = token_hex(8)
        return self.get_token(content=self.reset_token)

    @staticmethod
    def verify_password_reset(token):
        user, content = User.load_token(token)
        if user and user.reset_token == content:
            user.reset_token = None
            db.commit()
            return user
        return None

    @staticmethod
    def load_token(token):
        serializer = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = serializer.loads(token)["user_id"]
            content = serializer.loads(token)["content"]
        except SignatureExpired:
            return None, None
        return User.query.get(user_id), content

    def avatar(self, size=125):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size
        )

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Purchase(db.Model):
    """
    Table for purchases
    """

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    date = db.Column(
        db.DateTime, index=True, nullable=False, default=datetime.utcnow
    )
    image_file = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Purchase('{self.owner}', '{self.address}', '{self.date}')"
