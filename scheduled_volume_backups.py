import boto3
import schedule

ec2_client = boto3.client('ec2')

def create_volume_snapshots():
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['prod']
            }
        ]
    )

    for volume in volumes['volumes']:
        new_snapshot = ec2_client.create_snapshot(
            VolumeId=volume['VolumeId']
        )


schedule.every(5).minutes.do(create_volume_snapshots())
while True:
    schedule.run_pending()