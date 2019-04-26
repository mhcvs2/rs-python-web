from flask import Blueprint, request, jsonify
from app.common.response import Response, ResponseCodeEnum

api = Blueprint('api', __name__, url_prefix="/resource_manager")

from app.api.controllers import instance_resource_group, t1


@api.before_app_request
def before_request():
    user_id = request.cookies.get('user_id')
    if not user_id:
        return jsonify(Response(ResponseCodeEnum.NOT_LOGIN))
