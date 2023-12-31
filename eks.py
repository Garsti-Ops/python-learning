import boto3

client = boto3.client('eks')
clusters = client.list_clusters()

for cluster in clusters:
    response = client.describe_cluster(
        name=cluster
    )

    cluster_info = response['cluster']
    cluster_status = cluster_info['status']
    cluster_endpoint = cluster_info['endpoint']
    print(f"Cluster {cluster} status is {cluster_status}")
    print(f"Cluster endpoint: {cluster_endpoint}")
