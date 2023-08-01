import os

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - [%(threadName)s] - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': f"{os.environ.get('WORKDIR', '/app/papihub')}/logs/app.log",
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
