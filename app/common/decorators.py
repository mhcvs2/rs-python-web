# encoding: utf-8
from functools import wraps
from validator import validate as validator_validate
from flask import jsonify, wrappers, request
from .response import *
from .pagination import PaginatedDataView


def handle_exception(decorated):
    @wraps(decorated)
    def inner(*args, **kwargs):
        try:
            result = decorated(*args, **kwargs)
        except Exception as e:
            return jsonify(Response(ResponseCodeEnum.ERROR, e.message))
        if isinstance(result, Response):
            return jsonify(result)
        return result
    return inner


def _get_view_data_by_collection(view_class, collection):
    res = []
    for r in collection:
        res.append(view_class(r).data())
    if hasattr(view_class, 'name'):
        result_data = {
            '{}s'.format(getattr(view_class, 'name')): res
        }
    else:
        result_data = res
    return result_data


def simple_to_view(view_class):
    """
    :param view_class: view class
    :return: flask json response
    """
    def decorator(decorated):
        @wraps(decorated)
        def inner(*args, **kwargs):
            result = handle_exception(decorated)(*args, **kwargs)
            if isinstance(result, Response):
                return jsonify(result)
            if isinstance(result, wrappers.Response):
                return result
            if isinstance(result, list):
                result_data = _get_view_data_by_collection(view_class, result)
            elif isinstance(result, PaginatedDataView):
                result_data = _get_view_data_by_collection(view_class, result.collection)
                result_data['pagination'] = {
                    "page": result.page,
                    "total_record": result.total_count,
                    "page_size": result.page_size,
                    "total_page": result.total_page
                }
            else:
                view = view_class(result)
                result_data = view.data()
            return jsonify(Response(result=result_data))
        return inner
    return decorator


def validate(rules):
    def decorator(decorated):
        @wraps(decorated)
        def inner(*args, **kwargs):
            result = validator_validate(rules, request.json)
            if not result.valid:
                return jsonify(Response(ResponseCodeEnum.ERROR, str(result.errors)))
            return decorated(*args, **kwargs)
        return inner
    return decorator
