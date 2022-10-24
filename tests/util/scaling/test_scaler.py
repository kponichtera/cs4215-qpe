import unittest

from fltk.util.cluster.api_client import ClusterApiClient
from fltk.util.config.distributed_config import ScalingConfig
from fltk.util.scaling.scaler import ClusterScaler
from fltk.util.statistics.arrival_rate_estimator import Estimator


class MockEstimator(Estimator):

    def __init__(self, mock_arrival_time: float):
        self.mock_arrival_time = mock_arrival_time

    def estimate_arrival_rate(self) -> float:
        return self.mock_arrival_time


class MockClusterApiClient(ClusterApiClient):

    def __init__(self, current_node_pool_size) -> None:
        super().__init__()
        self.current_node_pool_size = current_node_pool_size

    def get_node_pool_size(self) -> int:
        return self.current_node_pool_size

    def set_node_pool_size(self, node_pool_size):
        self.current_node_pool_size = node_pool_size


class TestClusterScalerScaling(unittest.TestCase):

    def setUp(self):
        self.scaling_config = ScalingConfig(
            node_pool_name="mock",
            arrival_rate_thresholds=[1, 2, 3, 4, 5],
        )

    def test_minimum_scale(self):
        # given
        estimator = MockEstimator(0.5)
        cluster_api_client = MockClusterApiClient(2)

        cluster_scaler = ClusterScaler(self.scaling_config, estimator, cluster_api_client)

        # when
        cluster_scaler.scale()

        # then
        self.assertEquals(cluster_api_client.current_node_pool_size, 1)
