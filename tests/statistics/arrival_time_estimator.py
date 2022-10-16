import unittest

from fltk.util.statistics.arrival_time_estimator import ArrivalRateEstimator


class ArrivalRateEstimatorTest(unittest.TestCase):

    def setUp(self):
        self.estimator = ArrivalRateEstimator()

    def test_example(self):
        self.assertEquals(2, 2)
