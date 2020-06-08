import os
from unittest import TestCase, mock
from tempfile import TemporaryDirectory

from caproj import logger


class TestLoggingSetup(TestCase):
    """Test setup_logging function"""

    # def setUp(self):
    #     """Set up data for tests"""
    #     self.data = pd.DataFrame(
    #         {
    #             'x': [0, 1, 2, 3],
    #             'y': [2, 3, 4, 5]
    #         }
    #     )
    #     return super().setUp()

    def test_setup_logging_basicConfig(self):
        """Test setup_logging initializes with basicConfig"""
        with mock.patch(
            "caproj.logger.logging.basicConfig"
        ) as basicConfig_patch:
            logger.setup_logging(default_path='foo.json', env_key='foo')
            assert basicConfig_patch.called

    @mock.patch('caproj.logger.json.load')
    def test_setup_logging_dictConfig(self, mock_load):
        """Test setup_logging initializes with dictConfig from file"""
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "foo.json")
            open(fp, 'a').close()
            with mock.patch(
                'caproj.logger.logging.config.dictConfig'
            ) as dictConfig_patch:
                logger.setup_logging(default_path=fp, env_key='foo')
                assert dictConfig_patch.called
