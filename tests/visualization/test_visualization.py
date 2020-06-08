import os
from unittest import TestCase, mock
from tempfile import TemporaryDirectory

import pandas as pd
import matplotlib.pyplot as plt

from caproj import visualization as vis


class TestPlots(TestCase):
    """Test basic plotting functions"""

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
        with TemporaryDirectory():
            plt.plot(self.data['x'], self.data['y'])
            vis.save_plot(plt_object=plt, savepath=None)
            pass

    def test_plot_barplot(self):
        """Test plot_barplot function shows plot without error"""
        data = self.data['x'].value_counts()
        with mock.patch("caproj.visualization.plt.show") as show_patch:
            vis.plot_barplot(value_counts=data, title='test')
            assert show_patch.called

    # def test_plot_barplot_saves(self):
    #     """Test plot_barplot saves to file using savefile"""
    #     data = self.data['x'].value_counts()
    #     with TemporaryDirectory() as tmp:
    #         fp = os.path.join(tmp, 'test.png')
    #         vis.plot_barplot(value_counts=data, title='test', savepath=fp)
    #         assert os.path.exists(fp)
