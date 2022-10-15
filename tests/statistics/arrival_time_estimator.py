import unittest

from fltk.util.statistics.arrival_time_estimator import ArrivalTimeEstimator


class ArrivalTimeEstimatorTest(unittest.TestCase):

    def setUp(self):
        self.estimator = ArrivalTimeEstimator()

    def test_example(self):
        self.assertEquals(2, 2)
