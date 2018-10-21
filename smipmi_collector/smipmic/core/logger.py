import logging

from smipmic.core.config import ApplicationConfig


log_exception = logging.getLogger('smipmic').fatal


def configure():
    global log_exception
    logformat = r'{asctime:s}.{msecs:03.0f} [{levelname:8s}] {name:s}: {message:s}'
    dateformat = r'%a %d %b %Y %H:%M:%S'
    
    CONSOLE_LOGGER = logging.StreamHandler()
    CONSOLE_LOGGER.setFormatter(logging.Formatter(fmt=logformat, datefmt=dateformat, style='{'))
    
    _logging_conf = dict(
        handlers=[CONSOLE_LOGGER])
    _logging_conf['level'] = logging.DEBUG
    logging.basicConfig(**_logging_conf)
    if ApplicationConfig.DEBUG:
        CONSOLE_LOGGER.setLevel(logging.DEBUG)
        log_exception = logging.getLogger('smipmic').exception
    else:
        CONSOLE_LOGGER.setLevel(logging.INFO)
        log_exception = logging.getLogger('smipmic').error
