import logging

logger = None

def makeLogger(level="INFO"):
    logger = logging.getLogger('main')

    # Level
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logger.setLevel(numeric_level)

    ch = logging.StreamHandler()
    ch.setLevel(numeric_level)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def setupLogger(level="INFO"):
    global logger
    logger = makeLogger(level)

def getLogger():
    global logger

    if (logger is None):
        logger = makeLogger()

    return logger
