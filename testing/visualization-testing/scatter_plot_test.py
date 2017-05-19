import visualization.scatter_plot as scatter
import unittest
import random as r
import numpy as np

class TestScatter(unittest.TestCase):

    def setUp(self):
        self.random_points = [(r.randrange(-10, 10), r.randrange(-10, 10)) for x in range(100)]
        self.rgba_colors = np.zeros((100,4))
        self.rgba_colors[:,0]=1.0
        self.rgba_colors[:, 2] = [(x[0] + 10.0) / 20.0 for x in self.random_points]
        self.rgba_colors[:, 3] = [(x[1] + 10.0) / 20.0 for x in self.random_points]

    def test_basic(self):
        scatter.show_scatter(self.random_points)

    def test_color(self):
        scatter.show_scatter(self.random_points, color='r')

    def test_color_many(self):

        scatter.show_scatter(self.random_points, color=self.rgba_colors)

    def test_size(self):
        scatter.show_scatter(self.random_points, area=100)

    def test_size_many(self):
        scatter.show_scatter(self.random_points, area=[(x[1]+10)*100 for x in self.random_points])


if __name__ == '__main__':
    unittest.main()