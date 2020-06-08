import os
from unittest import TestCase, mock
from tempfile import TemporaryDirectory

from caproj import logger


class TestLoggingSetup(TestCase):
    """Test setup_logging function"""

    def setUp(self):
        """Set and clean up mock.patch objects for tests"""
        patcher = mock.patch('caproj.logger.json.load')
        self.mock_load = patcher.start()
        self.addCleanup(patcher.stop)

    def test_setup_logging_basicConfig(self):
        """Test setup_logging initializes with basicConfig"""
        with mock.patch(
            'caproj.logger.logging.basicConfig'
        ) as basicConfig_patch:
            logger.setup_logging(default_path='foo.json', env_key='foo')
            self.assertTrue(basicConfig_patch.called)

    def test_setup_logging_dictConfig(self):
        """Test setup_logging initializes with dictConfig from file"""
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, 'foo.json')
            open(fp, 'a').close()
            with mock.patch(
                'caproj.logger.logging.config.dictConfig'
            ) as dictConfig_patch:
                logger.setup_logging(default_path=fp, env_key='foo')
                self.assertTrue(dictConfig_patch.called)
