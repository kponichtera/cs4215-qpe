import logging
import time
from multiprocessing.pool import ThreadPool

from fltk.util.cluster.api_client import ClusterApiClient
from fltk.util.config.distributed_config import ScalingConfig
from fltk.util.statistics.arrival_time_estimator import Estimator


class ClusterScaler:
    SLEEP_TIME = 10

    def __init__(self, conf: ScalingConfig, estimator: Estimator, cluster_api_client: ClusterApiClient):
        self.__alive = False
        self.__thread_pool: ThreadPool = ThreadPool(processes=2)
        self._logger = logging.getLogger('ClusterScaler')

        self._arrival_time_thresholds = conf.arrival_rate_thresholds
        self._arrival_time_estimator = estimator
        self._cluster_api_client = cluster_api_client

        self.__last_scaling_time = 0
        self.__last_scale_down_time = 0

    def start(self):
        self._logger.info("Starting cluster scaler...")
        self.__alive = True
        self.__thread_pool.apply_async(self._run)

    def stop(self):
        self._logger.info("Stopping cluster scaler...")
        self.__alive = False
        self._logger.info("Successfully stopped cluster scaler")

    def _run(self):
        while self.__alive:
            self.scale()
            time.sleep(self.SLEEP_TIME)
        self._logger.info("Exiting ClusterScaler loop.")

    def scale(self):
        try:
            current_node_count = self._cluster_api_client.get_node_pool_size()
            required_node_count = self._determine_requested_node_count()

            if current_node_count != required_node_count:
                self._logger.info(f"Scaling cluster form {current_node_count} to {required_node_count} nodes")
                self._cluster_api_client.set_node_pool_size(required_node_count)

        except Exception as e:
            self._logger.error(f"Error when scaling the cluster. Reason: {e}")

    def _determine_requested_node_count(self) -> int:
        arrival_rate = self._arrival_time_estimator.estimate_arrival_rate()
        self._logger.debug(f"Current arrival rate: {arrival_rate}")

        # If arrival rate is smaller than the first threshold, keep only one node
        if arrival_rate < self._arrival_time_thresholds[0]:
            return 1

        # If arrival rate is between ith and i+1st threshold, return the amount of nodes that should be there
        for i in range(len(self._arrival_time_thresholds) - 1):
            if self._arrival_time_thresholds[i] < arrival_rate < self._arrival_time_thresholds[i+1]:
                return i + 2

        # If arrival rate is larger than the biggest threshold, return the maximum size of cluster
        if arrival_rate > self._arrival_time_thresholds[-1]:
            return len(self._arrival_time_thresholds) + 1