# Import all the modules and Libraries
import boto3
import schedule
import time
import datetime

# Open Management Console
aws_management_console = boto3.session.Session(profile_name="default")

# Open EC2 Console
ec2_console = aws_management_console.client(service_name = "ec2")

# Create EC2 Instance in eu-north-1 Region
response = ec2_console.run_instances(
    ImageId='#############',
    InstanceType='t3.micro',
    MaxCount=1,
    MinCount=1,
)

result = ec2_console.describe_instances()['Reservations']

# Get Instance ID
for each_instance in result:
    for value in each_instance['Instances']:
        print(value['InstanceId'])

# We use stop_instances method to stop instances
response = ec2_console.stop_instances(
    InstanceIds=['i-0ee69636e3c00049c']
)

# We use start_instances method to start instances
response = ec2_console.start_instances(
    InstanceIds=['i-0ee69636e3c00049c']
)

# Schedule Instance
def manage_instance():
    instance_id = 'i-0ee69636e3c00049c'

    def job():
        current_time = datetime.datetime.utcnow()
        current_day = current_time.weekday()
        current_hour = current_time.hour
        current_minute = current_time.minute

        allowed_days = [0, 2, 4, 6]  # Monday, Wednesday, Friday, Sunday

        if current_day in allowed_days and (9 <= current_hour < 11 or (current_hour == 11 and current_minute <= 30)):
            ec2_console.start_instance(instance_id)
        else:
            ec2_console.stop_instance(instance_id)

    # Schedule the job to run every minute
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    manage_instance()
