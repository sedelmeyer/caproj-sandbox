from unittest import TestCase, mock

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from caproj import visualization as vis


class TestSavePlot(TestCase):
    """Test save_plot function"""

    def setUp(self):
        self.data = pd.DataFrame(
            {
                'x': [0, 1, 2, 3],
                'y': [2, 3, 4, 5]
            }
        )
        return super().setUp()

    def tearDown(self):
        self.data.dispose()
        return super().tearDown()
