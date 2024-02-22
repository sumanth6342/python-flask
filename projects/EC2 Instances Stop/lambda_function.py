from datetime import datetime
import boto3
ec2 = boto3.client('ec2')


def lambda_handler(event, context):
    print(datetime.now().isoformat())

    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            },
        ]
    )

    instances_to_stop = []
    reservations = response["Reservations"]

    for reservation in reservations:
        instance_info = reservation["Instances"][0]

        instance_id = instance_info["InstanceId"]

        tags = instance_info["Tags"]
        name_of_the_instance = tags[0]['Value']

        current_state = instance_info["State"]['Name']

        if "dev" in name_of_the_instance:
            instances_to_stop.append(instance_id)

    if instances_to_stop:
        print(f"stopping {len(instances_to_stop)} instances")
        _ = ec2.stop_instances(
            InstanceIds=instances_to_stop
        )

    else:
        print("no instances to stop")
