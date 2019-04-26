import logging
from app.common.cfg import init_config
from oslo_config import cfg


CONF = cfg.CONF
init_config()


from app import create_app
app = create_app(CONF)


# @manager.command
# def test():
#     print "haha"


def main():
    from app.common.log import get_log_level
    debug = get_log_level() == logging.DEBUG
    app.run(CONF.server.ip, CONF.server.port, debug=debug)


if __name__ == '__main__':
    main()
