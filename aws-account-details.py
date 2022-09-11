#GETTING AWS ACCOUNT, ALIAS AND REGION WITH PYTHON
#export AWS_PROFILE=test

import os
import boto3

profile = os.environ['AWS_PROFILE']
aws = os.popen(''' aws sts get-caller-identity --query "Account" --output text --profile ''' + profile).read()
aws_account = aws.strip()
alias = boto3.client('iam').list_account_aliases()['AccountAliases'][0]
my_session = boto3.session.Session()
my_region = my_session.region_name

print("AWS Account ID is:", aws_account)
print("AWS Account ALIAS is:", alias)
print("AWS Account Region is:", my_region)
