import sys
import logging
from oslo_config import cfg


CONF = cfg.CONF

formetter_str = '[%(worker_name)s] %(asctime)s %(levelname)s pid=%(process)d: ' \
                '%(message)s %(funcName)s %(pathname)s:%(lineno)d'
formatter = logging.Formatter(formetter_str)
if CONF.log.log_file == "":
    console_handler = logging.StreamHandler(sys.stdout)
else:
    console_handler = logging.FileHandler(CONF.log.log_file)
console_handler.formatter = formatter

log_levels = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
}


class WorkerLogger(logging.LoggerAdapter):

    def __init__(self, logger, worker_name='conductor_worker', extra=None):
        self.worker_name = worker_name
        if not extra:
            extra = {}
        extra['worker_name'] = self.worker_name
        super(WorkerLogger, self).__init__(logger, extra)


def get_log_level():
    level = CONF.log.level
    return log_levels.get(level.upper())


Loggers = {}


def get_logger(worker_name="resource_manager"):
    if worker_name not in Loggers:
        logger = logging.getLogger(worker_name)
        logger.addHandler(console_handler)
        logger.setLevel(get_log_level())
        Loggers[worker_name] = WorkerLogger(logger, worker_name=worker_name)
    return Loggers[worker_name]
