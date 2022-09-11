'''
Export the Environment Variables before running the Script
export AWS_REGION=us-west-2
export AWS_PROFILE=test          #update your profile credentials in .aws/config file
'''

import boto3
import os
import sys
import time

REQUIRED_ENV_VARS = {"AWS_PROFILE", "AWS_REGION"}
diff = REQUIRED_ENV_VARS.difference(os.environ)
if len(diff) > 0:
    print('Failed because {} are not set'.format(diff))
    sys.exit(1)

env_var = os.environ
if {"RCX_BACKEND", "RCX_TENANT", "AWS_PROFILE", "AWS_REGION"} <= env_var.keys():
    profile = os.environ['AWS_PROFILE']
    region = os.environ['AWS_REGION']

#Variables
NAME = 'Vijay-EC2-Instance'
AMI_IMAGE_ID = 'ami-098e42ae54c764c35'       #Amazon-linux-2 ami-id in  us-west(oregon)
INSTANCE_TYPE = 't2.micro'
DISK_SIZE_GB = 8
DEVICE_NAME = '/dev/xvda'
SUBNET_ID = ''             #select subnet-id in which you want to launch instance
SECURITY_GROUPS_IDS = ['']     #select your sg samplesg
ELASTIC_IP = None                                  #If you need elastic ip to be attched to instance choose, ELASTIC_IP=True
ROLE_PROFILE = 'AWS-S3-ACCESS'
KEYPAIR = ''                           #create a keypair and give the name here
 
USERDATA_SCRIPT = """
#! /bin/bash
sudo yum update -y
sudo yum install -y httpd.x86_64
sudo systemctl start httpd.service
sudo systemctl enable httpd.service
echo -e "
<!DOCTYPE html>
<html>
<body>
<h1>Hello World !!</h1>
<p>Welcome to Vijay's Devops World</p>
</body>
</html>
" >> /var/www/html/index.html
sudo systemctl restart httpd.service 
"""
 
def create_ec2_client():
    print("================================================================================")
    print(f"Attempting to create EC2 Instance in {region} Region")
    session = boto3.Session(region_name=region, profile_name=profile)
    ec2_client = session.client('ec2')
    return ec2_client
 
 
def create_ec2_instance_with_tags():
 
    ec2_client = create_ec2_client()
    #session = create_ec2_client()
 
    blockDeviceMappings = [
        {
            'DeviceName': DEVICE_NAME,
            'Ebs': {
                'DeleteOnTermination': True,
                'VolumeSize': DISK_SIZE_GB,
                'VolumeType': 'gp2'
            }
        },
    ]
 
    # Create Elastic/Public IP for instance
    if ELASTIC_IP:
        networkInterfaces = [
            {
                'DeviceIndex': 0,
                'SubnetId': SUBNET_ID,
                'Groups': SECURITY_GROUPS_IDS,
                'AssociatePublicIpAddress': True,
                'DeleteOnTermination': True
            }, ]
        response = ec2_client.run_instances(ImageId=AMI_IMAGE_ID,
                                            InstanceType=INSTANCE_TYPE,
                                            NetworkInterfaces=networkInterfaces,
                                            MinCount=1, MaxCount=1,
                                            KeyName=KEYPAIR,
                                            BlockDeviceMappings=blockDeviceMappings,
                                            IamInstanceProfile={
                                              'Name': ROLE_PROFILE
                                                 },
                                            UserData=USERDATA_SCRIPT,
                                            TagSpecifications=[
                                                {
                                                    'ResourceType': 'instance',
                                                    'Tags': [
                                                        {
                                                            'Key': 'Name',
                                                            'Value': NAME
                                                        }
                                                    ]
                                                },
                                                {
                                                    'ResourceType': 'volume',
                                                    'Tags': [
                                                        {
                                                            'Key': 'Name',
                                                            'Value': NAME
                                                        }
                                                    ]
                                                }
                                            ])
        instance_id = response['Instances'][0]['InstanceId']
        print("Instance Id is:",instance_id)

        ec2_resource = boto3.Session(region_name=region, profile_name=profile).resource(service_name='ec2',region_name=region)
        instance = ec2_resource.Instance(id=instance_id)

        print("starting instance " + instance_id)
        instance.start()
        instance.wait_until_running()

        allocation = ec2_client.allocate_address(
        Domain='vpc',
        TagSpecifications=[
            {
                'ResourceType': 'elastic-ip',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': NAME
                    },
                ]
            },
        ]
        )
        
        eip=allocation["PublicIp"]
        aid=allocation["AllocationId"]
        print("Public IP is:",eip)
        print("Public IP's Assosiation Id is:",aid)
        time.sleep(10)
        eip_response = ec2_client.associate_address(AllocationId=aid,
                                     InstanceId=instance_id)
        #print(eip_response)
        print(f'EIP {eip} is associated with the instance {instance_id}')


    else:
        response = ec2_client.run_instances(ImageId=AMI_IMAGE_ID,
                                            InstanceType=INSTANCE_TYPE,
                                            SubnetId=SUBNET_ID,
                                            SecurityGroupIds=SECURITY_GROUPS_IDS,
                                            MinCount=1, MaxCount=1,
                                            KeyName=KEYPAIR,
                                            BlockDeviceMappings=blockDeviceMappings,
                                            IamInstanceProfile={
                                              'Name': ROLE_PROFILE
                                                 },
                                            UserData=USERDATA_SCRIPT,
                                            TagSpecifications=[
                                                {
                                                    'ResourceType': 'instance',
                                                    'Tags': [
                                                        {
                                                            'Key': 'Name',
                                                            'Value': NAME
                                                        }
                                                    ]
                                                },
                                                {
                                                    'ResourceType': 'volume',
                                                    'Tags': [
                                                        {
                                                            'Key': 'Name',
                                                            'Value': NAME
                                                        }
                                                    ]
                                                }
                                            ])
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        instance_id = response['Instances'][0]['InstanceId']
        ec2_client.get_waiter('instance_running').wait(
            InstanceIds=[instance_id]
        )
        print('Success!, instance with', instance_id, 'is created and running')
    else:
        print('Error! Failed to create instance!')
        raise Exception('Failed to create instance!')
 
    return instance_id
 
 
if __name__ == "__main__":
    create_ec2_instance_with_tags()
