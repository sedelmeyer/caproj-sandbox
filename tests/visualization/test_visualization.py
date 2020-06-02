import os
from unittest import TestCase, mock
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from caproj import visualization as vis


class TestSavePlot(TestCase):
    """Test save_plot function"""

    def setUp(self):
        """Set up data for tests"""
        self.data = pd.DataFrame(
            {
                'x': [0, 1, 2, 3],
                'y': [2, 3, 4, 5]
            }
        )
        return super().setUp()

    def test_save_plot(self):
        """Test save_plot function"""
        with TemporaryDirectory() as tmp:
            plt.plot(self.data['x'], self.data['y'])
            fp = os.path.join(tmp, 'test.png')
            vis.save_plot(plt_object=plt, savepath=fp)
            assert os.path.exists(fp)

    def test_save_plot_none(self):
        """Test save_plot function passes with no savepath"""
        with TemporaryDirectory() as tmp:
            plt.plot(self.data['x'], self.data['y'])
            vis.save_plot(plt_object=plt, savepath=None)
            assert not os.path.exists(fp)
