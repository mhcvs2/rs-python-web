# vim: tabstop=4 shiftwidth=4 softtabstop=4

from sqlalchemy.schema import Column
from sqlalchemy.schema import MetaData

from app.db.sqlalchemy.migrate_repo.schema import create_tables
from app.db.sqlalchemy.migrate_repo.schema import drop_tables
from app.db.sqlalchemy.migrate_repo.schema import Integer
from app.db.sqlalchemy.migrate_repo.schema import String
from app.db.sqlalchemy.migrate_repo.schema import Table


meta = MetaData()

test1 = Table(
    'test1',
    meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(255)),
    Column('age', Integer),
    )


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    create_tables([test1])


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    drop_tables([test1])
