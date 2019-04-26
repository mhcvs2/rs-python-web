from sqlalchemy import MetaData
from sqlalchemy import orm
from sqlalchemy.orm import exc as orm_exc
from sqlalchemy import Table


def map(engine):
    from app.db.data_models import instance_resource_group

    meta = MetaData()
    meta.bind = engine
    if mapping_exists(instance_resource_group.DBInstanceResourceGroup):
        return

    tables = {
        "instance_resource_group": instance_resource_group.DBInstanceResourceGroup,
    }

    for table_name, data_model in tables.items():
        orm.mapper(data_model, Table(table_name, meta, autoload=True))


def mapping_exists(model):
    try:
        orm.class_mapper(model)
        return True
    except orm_exc.UnmappedClassError:
        return False
