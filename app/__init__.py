from flask import Flask
from .db import get_db_api
from flask_cache import Cache
from config import Config


cache = Cache()


def init_db(conf):
    options = dict(
        sql_connection=conf.database.sql_connection,
        opts={}
    )
    get_db_api().configure_db(options)


def create_app(conf):
    from .common.log import get_logger
    log = get_logger()
    app = Flask(__name__)
    app.config.from_object(Config)
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    init_db(conf)
    cache.init_app(app)
    log.info("app start...")
    return app
