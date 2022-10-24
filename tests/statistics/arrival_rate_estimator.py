import time
import unittest

from fltk.util.statistics.arrival_rate_estimator import ArrivalRateEstimator


class ArrivalRateEstimatorTest(unittest.TestCase):

    def setUp(self):
        self.estimator = ArrivalRateEstimator()

    def test_2_arrivals(self):
        self.estimator.new_arrival()
        time.sleep(2)
        self.estimator.new_arrival()
        self.assertEquals(self.estimator.job_counter, 1)
        self.assertAlmostEqual(self.estimator.inter_arrival_sum, 2, 1)
        self.assertAlmostEqual(self.estimator.estimate_arrival_rate(), 0.5, 1)

    def test_3_arrivals(self):
        self.estimator.new_arrival()
        time.sleep(2)
        self.estimator.new_arrival()
        time.sleep(2)
        self.estimator.new_arrival()
        self.assertEquals(self.estimator.job_counter, 2)
        self.assertAlmostEqual(self.estimator.inter_arrival_sum, 4, 1)
        self.assertAlmostEqual(self.estimator.estimate_arrival_rate(), 0.5, 1)

    def test_3_different_arrivals(self):
        self.estimator.new_arrival()
        time.sleep(10)
        self.estimator.new_arrival()
        time.sleep(2)
        self.estimator.new_arrival()
        self.assertEquals(self.estimator.job_counter, 2)
        self.assertAlmostEqual(self.estimator.inter_arrival_sum, 12, 1)
        self.assertAlmostEqual(self.estimator.estimate_arrival_rate(), 0.166, 1)
