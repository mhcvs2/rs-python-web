import os
from oslo_config import cfg


CONF = cfg.CONF


class Config(object):

    CACHE_TYPE = 'simple'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:123@ali:3306/kbdp_console'
