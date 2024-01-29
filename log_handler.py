import logging.config
import os
from .config import get_conf

LOG_DIR = '/var/log'

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(filename)s %(lineno)s %(levelname)s %(message)s',
        },
        'access': {
            'format': '%(asctime)s %(message)s',
        }
    },
    'handlers': {
        'app': {
            'class': 'logging.FileHandler',
            'level': 20,
            'filename': os.path.join(get_conf()['log']['log_dir'], 'app.log') if get_conf() and 'log' in get_conf() and 'log_dir' in get_conf()['log'] else os.path.join(LOG_DIR, 'app.log'),
            'formatter': 'default',
        },
        'err': {
            'class': 'logging.FileHandler',
            'level': 20,
            'filename': os.path.join(get_conf()['log']['log_dir'], 'err.log') if get_conf() and 'log' in get_conf() and 'log_dir' in get_conf()['log'] else os.path.join(LOG_DIR, 'err.log'),
            'formatter': 'default',
        },
        'access': {
            'class': 'logging.FileHandler',
            'level': 20,
            'filename': os.path.join(get_conf()['log']['log_dir'], 'access.log') if get_conf() and 'log' in get_conf() and 'log_dir' in get_conf()['log'] else os.path.join(LOG_DIR, 'access.log'),
            'formatter': 'access',
        }
    },
    'loggers': {
        'app_log': {
            'handlers': ['app'],
            'level': 'INFO',
            'propagate': False,
        },
        'err_log': {
            'handlers': ['err'],
            'level': 'INFO',
            'propagate': False,
        },
        'access_log': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False,
        }
    },
    'disable_existing_loggers': True,
})


class Logger:
    def debug(self, data):
        logging.getLogger('app_log').info(data)

    def info(self, data):
        logging.getLogger('app_log').info(data)

    def error(self, data):
        logging.getLogger('err_log').error(data)


logger = Logger()
access_logger = logging.getLogger('access_log')
