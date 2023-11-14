import boto3

ec2_client = boto3.client('ec2')
ec2 = boto3.client('ec2')

instance_ids = []

reservations = ec2_client.describe_instaces()['Reservations']
for reservation in reservations:
    instances = reservation['Instances']
    for ins in instances:
        instance_ids.append(ins['InstanceId'])

response = ec2.create_tags(
    Resources=instance_ids,
    Tags=[{
        'Key': 'environment',
        'Value': 'dev'
    }]
)
