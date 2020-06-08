import os
from unittest import TestCase, mock
from tempfile import TemporaryDirectory

import pandas as pd
import matplotlib.pyplot as plt

from caproj import logger


class TestLoggingSetup(TestCase):
    """Test save_plot function"""

    # def setUp(self):
    #     """Set up data for tests"""
    #     self.data = pd.DataFrame(
    #         {
    #             'x': [0, 1, 2, 3],
    #             'y': [2, 3, 4, 5]
    #         }
    #     )
    #     return super().setUp()

    # def test_save_plot_none(self):
    #     """Test save_plot function passes with no savepath"""
    #     with TemporaryDirectory():
    #         plt.plot(self.data['x'], self.data['y'])
    #         vis.save_plot(plt_object=plt, savepath=None)
    #         pass

    def test_setup_logging_basicConfig(self):
        """Test plot_barplot function shows plot without error"""
        # data = self.data['x'].value_counts()
        with mock.patch("caproj.logger.logging.basicConfig") as basicConfig_patch:
            logger.setup_logging(default_path='foo.json', env_key='foo')
            assert basicConfig_patch.called
