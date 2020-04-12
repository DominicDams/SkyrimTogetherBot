import boto3

import time

f = open("aws_settings.conf",r)

region_name = f.readline()

RoleARN = f.readline()

f.close()

region_name='us-west-2'

client = boto3.client('cloudformation', region_name=region_name)

cloudformation = boto3.resource('cloudformation', region_name=region_name)

f = open("Cloudformation.yaml", "r")

template = f.read()

f.close()

result = client.create_stack(StackName='Skyim', TemplateBody=template, RoleARN='arn:aws:iam::460680689376:role/cloudformationserver', Capabilities=['CAPABILITY_IAM'])

print(result)

StackId = result['StackId']

stack = cloudformation.Stack(StackId)

status=stack.stack_status

while status != 'CREATE_COMPLETE':
  print(stack.stack_status)
  time.sleep(10)
  stack = cloudformation.Stack(StackId)
  status=stack.stack_status

print(stack.outputs)

instanceId = stack.outputs[0]['OutputValue']

f = open("Skyrim.creds", "w")

f.write(instanceId)

discord_key = input("Discord Key:")

f.write(discord_key)

f.write('\n')

f.close()
