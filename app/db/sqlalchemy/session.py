import contextlib
import threading

from oslo_db.sqlalchemy import session
import logging
from sqlalchemy import MetaData

from app.db.sqlalchemy import mappers

_FACADE = None
_LOCK = threading.Lock()


LOG = logging.getLogger(__name__)


def configure_db(options, models_mapper=None):
    facade = _create_facade(options)
    if models_mapper:
        models_mapper.map(facade)
    else:
        mappers.map(get_engine())


def _create_facade(options):
    global _LOCK, _FACADE
    if _FACADE is None:
        with _LOCK:
            if _FACADE is None:
                database_opts = options["opts"]
                _FACADE = session.EngineFacade(
                    options['sql_connection'],
                    **database_opts
                )
    return _FACADE


def _check_facade():
    if _FACADE is None:
        msg = "***The Database has not been setup!!!***"
        LOG.exception(msg)
        raise RuntimeError(msg)


def get_facade():
    _check_facade()
    return _FACADE


def get_engine(use_slave=False):
    _check_facade()
    return _FACADE.get_engine(use_slave=use_slave)


def get_session(**kwargs):
    return get_facade().get_session(**kwargs)


def raw_query(model, **kwargs):
    return get_session(**kwargs).query(model)


def clean_db():
    engine = get_engine()
    meta = MetaData()
    meta.bind = engine
    meta.reflect()
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            if table.name != "migrate_version":
                con.execute(table.delete())
        trans.commit()


def drop_db(options):
    if options:
        _create_facade(options)
    engine = get_engine()
    meta = MetaData()
    meta.bind = engine
    meta.reflect()
    meta.drop_all()
