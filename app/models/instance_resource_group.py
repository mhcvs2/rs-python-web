# coding: utf-8
from sqlalchemy import Column, DateTime, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT
from sqlalchemy.ext.declarative import declarative_base
from app import db

Base = declarative_base()
metadata = Base.metadata


class InstanceResourceGroup(Base):
    __tablename__ = 'instance_resource_group'
    _data_fields = ['id', 'user_id', 'region_code', 'product_type_id', 'gp_name', 'item_no', 'value_max',
                    'value_min', 'description', 'status', 'create_time', 'update_time', 'resource_conf',
                    'is_default', 'value_dev', 'value_prod']

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(BIGINT(11), nullable=False)
    region_code = Column(String(50), nullable=False)
    product_type_id = Column(INTEGER(11), nullable=False)
    gp_name = Column(String(50), nullable=False)
    item_no = Column(String(255))
    value_max = Column(INTEGER(11))
    value_min = Column(INTEGER(11))
    description = Column(String(255))
    status = Column(SMALLINT(6), server_default=text("'1'"))
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    resource_conf = Column(String(255))
    is_default = Column(INTEGER(11), server_default=text("'0'"))
    value_dev = Column(INTEGER(11))
    value_prod = Column(INTEGER(11))

    @staticmethod
    def get_by_id(group_id):
        return db.session.query(InstanceResourceGroup).filter_by(id=group_id).first()
