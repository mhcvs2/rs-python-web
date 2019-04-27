import sqlalchemy.exc

from app.common import exception
from app.db.sqlalchemy import session
from app.db.sqlalchemy import migration


def list(query_func, *args, **kwargs):
    return query_func(*args, **kwargs).all()


def count(query, *args, **kwargs):
    return query(*args, **kwargs).count()


def first(query, *args, **kwargs):
    return query(*args, **kwargs).first()


def join(query, model, *args):
    return query(model).join(*args)


def order_by(query, model, conditions, *args):
    return query(model).filter_by(**conditions).order_by(*args)

# noinspection PyShadowingBuiltins


def filter(query, model, conditions, *args):
    return query(model).filter_by(**conditions).filter(*args)


def find_all(model, **conditions):
    return _query_by(model, **conditions)


def find_all_by_limit(query_func, model, conditions, limit, marker=None,
                      marker_column=None):
    return _limits(query_func, model, conditions, limit, marker,
                   marker_column).all()


def find_all_by_query_limit(query, limit, marker=None,
                            marker_column=None):
    return __limits(query, limit, marker,
                    marker_column).all()


def find_by(model, **kwargs):
    return _query_by(model, **kwargs).first()


def find_by_filter(model, **kwargs):
    filters = kwargs.pop('filters', [])
    return _query_by_filter(model, *filters, **kwargs)


def save(model):
    try:
        db_session = session.get_session()
        model = db_session.merge(model)
        db_session.flush()
        return model
    except sqlalchemy.exc.IntegrityError as error:
        raise exception.DBConstraintError(model_name=model.__class__.__name__,
                                          error=str(error.orig))


def delete(model):
    db_session = session.get_session()
    model = db_session.merge(model)
    db_session.delete(model)
    db_session.flush()


def delete_all(query_func, model, **conditions):
    query_func(model, **conditions).delete()


def update(model, **values):
    for k, v in values.items():
        model[k] = v


def update_all(query_func, model, conditions, values):
    query_func(model, **conditions).update(values)


def configure_db(options, *plugins):
    session.configure_db(options)
    configure_db_for_plugins(options, *plugins)


def configure_db_for_plugins(options, *plugins):
    for plugin in plugins:
        session.configure_db(options, models_mapper=plugin.mapper)


def drop_db(options):
    session.drop_db(options)


def clean_db():
    session.clean_db()


def _base_query(cls):
    return session.get_session().query(cls)


def _query_by(cls, **conditions):
    query = _base_query(cls)
    if conditions:
        query = query.filter_by(**conditions)
    return query


def _query_by_filter(cls, *filters, **conditions):
    query = _query_by(cls, **conditions)
    if filters:
        query = query.filter(*filters)
    return query


def _limits(query_func, model, conditions, limit, marker, marker_column=None):
    query = query_func(model, **conditions)
    marker_column = marker_column or model.id
    if marker:
        query = query.filter(marker_column > marker)
    return query.order_by(marker_column).limit(limit)


def __limits(query, limit, marker, marker_column=None):
    if marker_column:
        query = query.order_by(marker_column)
    if marker:
        if not isinstance(marker, int) and marker_column:
            query = query.filter(marker_column > marker)
        else:
            query = query.offset(marker)
    return query.limit(limit)


def db_sync(options, version=None, repo_path=None):
    migration.db_sync(options, version, repo_path)


def db_upgrade(options, version=None, repo_path=None):
    migration.upgrade(options, version, repo_path)


def db_downgrade(options, version, repo_path=None):
    migration.downgrade(options, version, repo_path)


def db_reset(options, *plugins):
    drop_db(options)
    db_sync(options)
    configure_db(options)
