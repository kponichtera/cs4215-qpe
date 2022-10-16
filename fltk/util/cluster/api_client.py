import abc

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

    def __init__(self, conf: ScalingConfig):
        super().__init__()
        self._container_client = container_v1.ClusterManagerClient()
        self._node_pool_name = conf.node_pool_name
        pass

    def get_node_pool_size(self) -> int:
        request = container_v1.GetNodePoolRequest()
        request.name = self._node_pool_name

        response = self._container_client.get_node_pool(request=request)

        return response.initial_node_count

    def set_node_pool_size(self, node_count):
        request = container_v1.SetNodePoolSizeRequest()
        request.name = self._node_pool_name
        request.node_count = node_count

        response = self._container_client.set_node_pool_size(request=request)
