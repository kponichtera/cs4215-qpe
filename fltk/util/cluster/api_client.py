import abc
import logging
import time

from google.cloud import container_v1

from fltk.util.config.distributed_config import ScalingConfig


class ClusterApiClient:

    @abc.abstractmethod
    def get_node_pool_size(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def set_node_pool_size(self, node_pool_size):
        raise NotImplementedError()


class GKEClusterApiClient(ClusterApiClient):
    SCALING_TIMEOUT = 120
    SCALING_SLEEP = 10

    def __init__(self, conf: ScalingConfig):
        super().__init__()
        self._logger = logging.getLogger('GKEClusterApiClient')
        self._container_client = container_v1.ClusterManagerClient()
        self._node_pool_name = conf.node_pool_name
        pass

    def get_node_pool_size(self) -> int:
        request = container_v1.GetNodePoolRequest()
        request.name = self._node_pool_name

        response = self._container_client.get_node_pool(request=request)

        return response.initial_node_count

    def set_node_pool_size(self, requested_node_count):
        request = container_v1.SetNodePoolSizeRequest()
        request.name = self._node_pool_name
        request.node_count = requested_node_count

        self._logger.info(f"Requesting cluster scaling to {requested_node_count} nodes")
        self._container_client.set_node_pool_size(request=request)

        start_time = time.time()
        while time.time() - start_time < self.SCALING_TIMEOUT:
            time.sleep(self.SCALING_SLEEP)
            node_count = self.get_node_pool_size()
            if node_count == requested_node_count:
                break
            self._logger.info(f"Waiting for cluster scaling to finish ({node_count}/{requested_node_count} nodes)...")
        self._logger.info(f"Scaling to {requested_node_count} complete after {time.time() - start_time} seconds")
