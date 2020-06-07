"""
caproj.logger
~~~~~~~~~~~~~

This module handles setup of logging configuration for ``caproj`` package
"""

import os
import sys
import json
import logging
import logging.config


def setup_logging(
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
