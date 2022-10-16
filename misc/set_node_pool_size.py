from google.cloud import container_v1

client = container_v1.ClusterManagerClient()

########################################################################################################################

request = container_v1.SetNodePoolSizeRequest()
request.name = "projects/test-bed-fltk-kponichtera/locations/us-central1-c/clusters/fltk-testbed-cluster/nodePools/medium-fltk-pool-1"
request.node_count = 2

response = client.set_node_pool_size(request=request)

print(response)

########################################################################################################################


request = container_v1.GetNodePoolRequest()
request.name = "projects/test-bed-fltk-kponichtera/locations/us-central1-c/clusters/fltk-testbed-cluster/nodePools/medium-fltk-pool-1"

response = client.get_node_pool(request=request)

print(response.initial_node_count)

