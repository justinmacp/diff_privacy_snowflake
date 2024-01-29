from flask import Flask
from postgresql_src.api.config import Config
from flask_migrate import Migrate
from postgresql_src.api.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="My_Secret_Key"
    )

    app.config.from_object(Config)

    # Database related part
    db.init_app(app)
    migrate = Migrate(app, db)

    return app
