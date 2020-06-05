"""
This module contains the sets base logger and logging functions used
throughout ``caproj``
"""

import logging
import time
from functools import wraps

log_file = '{}.log'.format(__name__)
log_level = logging.INFO
logging.basicConfig(
    level=log_level, filename=log_file, filemode="w+",
    format="%(asctime)-15s %(levelname)-8s %(message)s"
    )


def log_func(orig_func):

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        logging.info('Run function {}'.format(orig_func.__name__))
        logging.info(
            'Ran with args: {}, and kwargs: {}'.format(args, kwargs)
            )
        logging.info(orig_func.__doc__.partition('\n')[0])
        result = orig_func(*args, **kwargs)
        logging.info(
            '{} ran in: {} sec'.format(orig_func.__name__, time.time() - t1)
            )
        return result

    return wrapper


def timer(orig_func):

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        logging.info('{} ran in: {} sec'.format(orig_func.__name__, t2))
        return result

    return wrapper

    © 2020 GitHub, Inc.
    Terms
    Privacy
