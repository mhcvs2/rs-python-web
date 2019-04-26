import logging
from app import create_app
from app.common.cfg import init_config
from oslo_config import cfg
from app.common.log import get_log_level


CONF = cfg.CONF
init_config()


app = create_app(CONF)


# @manager.command
# def test():
#     print "haha"


if __name__ == '__main__':
    debug = get_log_level() == logging.DEBUG
    app.run(CONF.server.ip, CONF.server.port, debug=debug)
