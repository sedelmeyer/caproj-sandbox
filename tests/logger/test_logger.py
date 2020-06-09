import logging
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


class TestLogFunc(TestCase):
    """Test logfunc logging decorator"""
    log = logging.getLogger('test')

    @logger.logfunc(
        log=log, funcname=True, docdescr=True, argvals=True, runtime=True
    )
    def test_func(self, **kwargs):
        """Decorated test function for testing logfunc"""
        pass

    def test_logfunc_logs(self):
        """Ensure logfunc provides all logs"""
        with self.assertLogs('test', level='INFO') as logmsg:
            self.test_func(kwarg1='foo', kwarg2='bar')
            self.assertTrue(len(logmsg.output) == 4)
