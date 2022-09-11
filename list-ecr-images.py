'''
Export the Environment Variables before running the Script
export AWS_REGION=us-west-2
export AWS_PROFILE=test          #update your profile credentials in .aws/config file
'''
#PYTHON SCRIPT TO CHECK WHETHER IMAGE EXISTS IN ECR OR NOT

import os
import sys
import boto3

REQUIRED_ENV_VARS = {"AWS_PROFILE", "AWS_REGION"}
diff = REQUIRED_ENV_VARS.difference(os.environ)
if len(diff) > 0:
    print('Failed because {} are not set'.format(diff))
    sys.exit(1)

env_var = os.environ
if {"AWS_PROFILE", "AWS_REGION"} <= env_var.keys():
    profile = os.environ['AWS_PROFILE']
    region = os.environ['AWS_REGION']

def custom_msg(msg):
    row = len(msg)
    h = ''.join(['+'] + ['-' *row] + ['+'])
    result= h + '\n'"|"+msg+"|"'\n' + h
    print(result)

def create_ec2_client():
      try:
          print(f"Checking ECR image in AWS {region} Region")
          repo=input("Enter Repository Name: ")
          tag=input("Enter the Tag: ")
          session = boto3.Session(region_name=region, profile_name=profile)
          client = session.client('ecr')
          cred = session.client('ecr').get_authorization_token()['authorizationData'][0]
          ecr_url = cred['proxyEndpoint']
          ecr_reg_id = ecr_url.replace('https://', '').split('.')[0]
          response = client.describe_images(
          registryId=ecr_reg_id,
          repositoryName=repo,
          imageIds=[
             {
                 'imageTag': tag
             },
           ],
          filter={
              'tagStatus': 'ANY'
           }
           )
          print(f"{ecr_reg_id}.dkr.ecr.{region}.amazonaws.com/{repo}:{tag}")
          custom_msg(f"Image Exists in {region}")

      except Exception as error:
            print(f"{ecr_reg_id}.dkr.ecr.{region}.amazonaws.com/{repo}:{tag}")
            custom_msg(f"Image doesn't Exists in {region}")

create_ec2_client()
