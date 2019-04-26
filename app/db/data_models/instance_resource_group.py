from app.db.models import DatabaseModelBase


class DBInstanceResourceGroup(DatabaseModelBase):
    _data_fields = ['id', 'user_id', 'region_code', 'product_type_id', 'gp_name', 'item_no', 'value_max',
                    'value_min', 'description', 'status', 'create_time', 'update_time', 'resource_conf',
                    'is_default', 'value_dev', 'value_prod']
