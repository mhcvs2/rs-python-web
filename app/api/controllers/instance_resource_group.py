from flask import request
from app.api import api
from app.common.decorators import validate
from app.api.services.instance_resource_group import InstanceResourceGroupService
from app.api.validators.instance_resource_group import add_rules


@api.route('/groups', methods=['GET'])
def list():
    return InstanceResourceGroupService.list()


@api.route('/groups/<int:group_id>', methods=['GET'])
def get(group_id):
    return InstanceResourceGroupService.get(group_id)


@api.route('/groups', methods=['POST'])
@validate(add_rules)
def add():
    request.json['user_id'] = request.cookies.get('user_id')
    return InstanceResourceGroupService.add(request.json)
