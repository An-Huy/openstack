import logging
from logging.handlers import TimedRotatingFileHandler
from common.config import load_config

CONF = load_config("logging")

MAP_LOGLEVEL = {'debug': logging.DEBUG,
                'warning': logging.WARNING,
                'info': logging.INFO,
                'critical': logging.CRITICAL,
                'error': logging.ERROR}

def setup_logging(name):
    logger = logging.getLogger(name)
    logger.setLevel(MAP_LOGLEVEL[CONF['log_level']])

    # create the logging file handler
    FILEPATH = CONF['log_file']
    fh = TimedRotatingFileHandler(FILEPATH, when='D', backupCount=30)
    formatter = logging.Formatter("%(asctime)s [ %(levelname)s ] %(message)s")

    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    return logger

if __name__ == "__main__":
    LOG = setup_logging(__name__)
    LOG.info("Welcome to  Logging")
    LOG.debug("A debugging message")
    LOG.warning("A warning occurred")
    LOG.error("An error occurred")
    LOG.exception("An Exception occurred")