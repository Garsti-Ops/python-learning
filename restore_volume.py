from operator import itemgetter
import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

instance_id = 'testmydude'

volumes = ec2_client.describe_volumes(
    Filters=[{
        'Name': 'attachement.instance_id',
        'Value': [instance_id]
    }]
)

instance_volume = volumes['Volumes'][0]

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[{
        'Name': 'volume-id',
        'Values': [instance_volume['VolumeIde']]
    }]
)

latest_snapshot = sorted(snapshots, key=itemgetter('StartTime'), reverse=True)[0]
new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone="",
    TagSpecification=[
        {
            'ResourceType': 'volume',
            'Tags': [{
                'Key': 'Name',
                'Value': 'prod'
            }]
        }
    ]
)

ec2_resource.Instance(instance_id).attach_volume(
    VolumeId=new_volume['VolumeId'],
    Device='/dev/xvdb'
)
