from flask import request
from app.common.log import get_logger
from app.db.data_models.instance_resource_group import DBInstanceResourceGroup
from app.api.views.instance_resource_group import InstanceResourceGroupView
from app.common.decorators import simple_to_view, handle_exception
from app.common.response import Response


log = get_logger()


class InstanceResourceGroupService(object):

    @classmethod
    @simple_to_view(InstanceResourceGroupView)
    def list(cls):
        user_id = request.cookies.get('user_id')
        log.info("list groups for user: %s", user_id)
        page = request.args.get('page', 1)
        page_size = request.args.get('page_size', 10)
        groups = DBInstanceResourceGroup.find_all(user_id=user_id)
        data = DBInstanceResourceGroup.find_by_page(groups, page, page_size, marker_column=DBInstanceResourceGroup.id)
        return data

    @classmethod
    @simple_to_view(InstanceResourceGroupView)
    def get(cls, group_id):
        user_id = request.cookies.get('user_id')
        log.info("list group(id=%s) for user: %s", group_id, user_id)
        group = DBInstanceResourceGroup.find_by(id=group_id, user_id=user_id)
        return group

    @classmethod
    @handle_exception
    def add(cls, data):
        data['value_max'] = data['value_dev'] + data['value_prod']
        DBInstanceResourceGroup.create(**data)
        return Response()
