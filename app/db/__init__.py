from app.db.sqlalchemy import api as db_api


def get_db_api():
    return db_api


class Query(object):
    """Mimics sqlalchemy query object.

    This class allows us to store query conditions and use them with
    bulk updates and deletes just like sqlalchemy query object.
    Using this class makes the models independent of sqlalchemy

    """

    def __init__(self, model, query_func, query=None, **conditions):
        self._query_func = query_func
        self._model = model
        self._conditions = conditions
        self.db_api = db_api
        self.query = query

    def all(self):
        return self.db_api.list(self._query_func, self._model,
                                **self._conditions)

    def count(self):
        if self.query:
            return self.query.count()
        return self.db_api.count(self._query_func, self._model,
                                 **self._conditions)

    def first(self):
        return self.db_api.first(self._query_func, self._model,
                                 **self._conditions)

    def join(self, *args):
        return self.db_api.join(self._query_func, self._model, self._conditions, *args)

    def order_by(self, *args):
        return self.db_api.order_by(self._query_func, self._model, self._conditions, *args)

    def filter(self, *args):
        return self.db_api.filter(self._query_func, self._model, self._conditions, *args)

    def __iter__(self):
        return iter(self.all())

    def update(self, **values):
        self.db_api.update_all(self._query_func, self._model, self._conditions,
                               values)

    def delete(self):
        self.db_api.delete_all(self._query_func, self._model,
                               **self._conditions)

    def limit(self, limit=200, marker=None, marker_column=None):
        if self.query:
            return self.db_api.find_all_by_query_limit(self.query, limit, marker, marker_column)
        return self.db_api.find_all_by_limit(
            self._query_func,
            self._model,
            self._conditions,
            limit=limit,
            marker=marker,
            marker_column=marker_column)

    def paginated_collection(self, limit=200, marker=None, marker_column=None):
        if marker:
            try:
                marker = int(marker)
            except ValueError:
                pass
        total_count = self.count()
        collection = self.limit(int(limit) + 1, marker, marker_column)
        if len(collection) > int(limit):
            if not isinstance(marker, int):
                return collection[0:-1], collection[-2]['id'], total_count
            else:
                return collection[0:-1], marker + limit, total_count
        return collection, None, total_count

    def paginated_collection2(self, limit, marker, marker_column=None, **kwargs):
        marker = int(marker)
        total_count = self.count()
        collection = self.order_by(marker_column).all()
        start = marker
        end = marker + limit
        if len(collection) > end:
            return collection[start:end], end, total_count
        return collection[start:], None, total_count


class Queryable(object):

    def __getattr__(self, item):
        return lambda model, **conditions: Query(
            model, query_func=getattr(db_api, item), **conditions)


db_query = Queryable()
