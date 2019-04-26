from flask import Flask
from .db import get_db_api


def init_db(conf):
    options = dict(
        sql_connection=conf.database.sql_connection,
        opts={}
    )
    get_db_api().configure_db(options)


def create_app(conf):
    app = Flask(__name__)
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    init_db(conf)
    return app
