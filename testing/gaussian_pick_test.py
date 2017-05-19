import visualization.scatter_plot as scatter
import gaussian_pick as gaus
import unittest
import random as r
import numpy as np

class TestScatter(unittest.TestCase):

    def setUp(self):
        pass

    def test_far(self):
        self.points = gaus.generate_neuron_input_points(50, 50, 50, 50, 100, 100, 2000)
        scatter.show_scatter(self.points)

    def test_normal(self):

        self.points = gaus.generate_neuron_input_points(50, 50, 20, 20, 100, 100, 2000)
        scatter.show_scatter(self.points)

    def test_close(self):
        # fail
        self.points = gaus.generate_neuron_input_points(50, 50, 0, 0, 100, 100, 2000)
        scatter.show_scatter(self.points)


if __name__ == '__main__':
    unittest.main()