import sys
from oslo_config import cfg


CONF = cfg.CONF


database_opts = [
    cfg.StrOpt('sql_connection',
               default="mysql://root:123@ali:3306/db_test",
               help='sql_connection'),
]

server_opts = [
    cfg.StrOpt('ip',
               default="0.0.0.0",
               help='server ip'),
    cfg.PortOpt('port',
                default=5000,
                help='server host')
]

log_opts = [
    cfg.StrOpt('level',
               default="info",
               help='log level NOTSET/DEBUG/INFO/WARNING/ERROR/CRITICAL'
               ),
]


def init_config():
    argv = sys.argv
    CONF.register_opts(database_opts, 'database')
    CONF.register_opts(log_opts, 'log')
    CONF.register_opts(server_opts, 'server')
    CONF(args=argv[1:],
         project='resource_manager',
         version="0.0.1",
         default_config_files=["/etc/resource_manager.conf"])
