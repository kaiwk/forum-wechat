import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.info)

    handler = logging.FileHandler('/var/log/flask/{}.log'.format(name))
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    return logger
