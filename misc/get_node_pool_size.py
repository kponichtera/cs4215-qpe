from google.cloud import container_v1

client = container_v1.ClusterManagerClient()

########################################################################################################################

request = container_v1.GetNodePoolRequest()
request.name = "projects/qpe2022project/locations/us-central1-c/clusters/fltk-testbed-cluster/nodePools/medium-fltk-pool-1"

response = client.get_node_pool(request=request)

print(response.initial_node_count)

