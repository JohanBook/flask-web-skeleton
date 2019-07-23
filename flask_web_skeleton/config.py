import os


class Config:
    SECRET_KEY = "9c4c971e249b5f90558bf749515acc8c"  # move to env variable
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABSE_URL") or "sqlite:///site.db"
    )  # move to env variable
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
