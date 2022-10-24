import logging
import time
from multiprocessing.pool import ThreadPool

from fltk.util.cluster.api_client import ClusterApiClient
from fltk.util.config.distributed_config import ScalingConfig
from fltk.util.statistics.arrival_rate_estimator import Estimator


class ClusterScaler:
    SLEEP_TIME = 10

    def __init__(self, conf: ScalingConfig, estimator: Estimator, cluster_api_client: ClusterApiClient):
        self._alive = False
        self._thread_pool: ThreadPool = ThreadPool(processes=2)
        self._logger = logging.getLogger('ClusterScaler')

        self._dry_run = conf.dry_run
        self._arrival_time_thresholds = conf.arrival_rate_thresholds
        self._scale_down_grace_period = conf.scale_down_grace_period
        self._arrival_rate_estimator = estimator
        self._cluster_api_client = cluster_api_client

        self._last_scaling_time = 0
        self._last_scale_down_time = 0

    def start(self):
        self._logger.info("Starting cluster scaler...")
        self._alive = True
        self._thread_pool.apply_async(self._run)

    def stop(self):
        self._logger.info("Stopping cluster scaler...")
        self._alive = False
        self._logger.info("Successfully stopped cluster scaler")

    def _run(self):
        while self._alive:
            self.scale()
            time.sleep(self.SLEEP_TIME)
        self._logger.info("Exiting ClusterScaler loop.")

    def scale(self):
        try:
            current_node_count = self._cluster_api_client.get_node_pool_size()
            required_node_count = current_node_count + self._determine_requested_node_count()

            now = time.time()
            scale_down = required_node_count < current_node_count

            if current_node_count == required_node_count:
                self._logger.info(f"No cluster scaling is necessary")
            elif scale_down and now - self._last_scaling_time < self._scale_down_grace_period:
                self._logger.info(f"Waiting grace period before scaling down from {current_node_count} to {required_node_count} nodes...")
            elif self._dry_run:
                self._logger.info(f"DRY RUN - would scale cluster from {current_node_count} to {required_node_count} nodes")
            else:
                if scale_down:
                    self._last_scaling_time = now
                self._logger.info(f"Scaling cluster from {current_node_count} to {required_node_count} nodes")
                self._cluster_api_client.set_node_pool_size(required_node_count)

        except Exception as e:
            self._logger.error(f"Error when scaling the cluster. Reason: {e}")

    def _determine_requested_node_count(self) -> int:
        ratio = self._arrival_rate_estimator.estimate_arrival_rate() / self._arrival_rate_estimator.estimate_service_rate()
        self._logger.debug(f"Current arrival rate and service rate ratio: {ratio}")

        # If the ratio is smaller than the lower threshold => scale down 1 node
        if ratio < self._arrival_time_thresholds[0]:
            return - 1
        # If the ratio is greater than the upper threshold => scale up 1 node
        elif ratio > self._arrival_time_thresholds[1]:
            return 1
        # If the utilization is between 0.7 and 0.8 => keep the current number of nodes
        else:
            return 0
