"""
caproj.logger
~~~~~~~~~~~~~

This module contains logging-related features for the ``caproj`` package

**Module functions:**

.. autosummary::
   logfunc
   start_logging

|
"""

import functools
import json
import logging
import logging.config
import os
import sys
import time


def start_logging(
    default_path='logging.json',
    default_level='INFO',
    env_key='LOG_CFG'
):
    """Set up logging configuration for ``caproj`` package

    :param default_path: string file path for json formatted
                         logging configuration file (default is
                         'logging.json')
    :param default_level: string indicating the default level
                          for logging, accepts the following
                          values: 'DEBUG', 'INFO', 'WARNING',
                          'ERROR', 'CRITICAL' (default is 'INFO')
    :param env_key: string indicating environment key if one exists
                    (default is 'LOG_CFG')
    """
    path = default_path
    value = os.getenv(env_key, None)
    default_level = default_level.upper()
    level = eval('logging.{}'.format(default_level))

    if value:
        path = value

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)

        log = logging.getLogger(__name__)
        log.info('logging configured using {}'.format(path))

    else:
        logging.basicConfig(
            level=level,
            stream=sys.stdout,
            format="%(levelname)s: %(name)s: %(message)s"
            )

        log = logging.getLogger(__name__)
        log.info(
            'logging configured using basicConfig, level={}'.format(
                default_level
            )
        )


def logfunc(orig_func=None, log=None,
            funcname=False, argvals=False,
            docdescr=False, runtime=False):
    """Wrap function call to provide log information when function is called

    This function acts as a ``functools.wraps`` decorator for decorating
    functions or methods to provide logging functionality to log details
    of the decorated function

    :param orig_func: NoneType placeholder parameter
    :param log: logging.getLogger object for logging, default is None
    :param funcname: boolean indicating whether to log name of function,
                     default is False
    :param argvals: boolean indicating whether to log function arguments,
                    default is False
    :param docdescr: boolean indicating whether to log function docstring
                     short description, default is False
    :param runtime: boolean indicating whether to log function execution
                    runtime in seconds, default is False
    :return: ``functools.wraps`` wrapper function

    .. note:: All logs are generate at the 'INFO' logging level

    Example::
        log = logging.getLogger(__name__)
        @logfunc(log=log, funcname=True, runtime=True)
        def some_function(arg1, **kwargs):
            ...
    """

    if not orig_func:
        return functools.partial(
            logfunc, log=log,
            funcname=funcname, argvals=argvals,
            docdescr=docdescr, runtime=runtime
        )

    @functools.wraps(orig_func)
    def wrapper(*args, **kwargs):

        if funcname:
            log.info('Run function {}'.format(orig_func.__name__))

        if docdescr:
            log.info(orig_func.__doc__.partition('\n')[0])

        if argvals:
            log.info(
                'Run with args: {}, and kwargs: {}'.format(args, kwargs)
            )

        if runtime:
            t1 = time.time()
            result = orig_func(*args, **kwargs)
            t2 = time.time() - t1
            log.info('{} run time: {:.3f} sec'.format(orig_func.__name__, t2))
            return result

        else:
            return orig_func(*args, **kwargs)

    return wrapper
