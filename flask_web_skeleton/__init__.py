from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_web_skeleton.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

login_manger = LoginManager()
login_manger.login_view = "users.login"
login_manger.login_message_category = "danger"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from flask_web_skeleton.errors.handlers import errors
    from flask_web_skeleton.api.routes import api
    from flask_web_skeleton.main.routes import main
    from flask_web_skeleton.users.routes import users

    app.register_blueprint(api)
    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(users)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manger.init_app(app)
    mail.init_app(app)

    migrate = Migrate(app, db)

    with app.app_context():
        tables = db.get_tables_for_bind()
        if not tables:
            print(
                f"Unable to locate tables, got {tables}. Creating new tables."
            )

        else:
            print(f"Found tables: {tables}")
        db.create_all()

    return app
