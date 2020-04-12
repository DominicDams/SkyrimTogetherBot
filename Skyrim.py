import discord
import boto3

f = open("Skyrim.creds", "r")

instance_id = f.readline().rstrip()

discord_token = f.readline().rstrip()

f.close()

client = discord.Client()
ec2 = boto3.client('ec2', region_name='us-west-2')
ec2_resource = boto3.resource('ec2', region_name='us-west-2')
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):    
    if message.author == client.user:
        return

    if message.content == '!skyrim start':
        print(message.content)
        try:
            ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
            await message.channel.send('Starting server!')
        except Exception as e:
            await message.channel.send('Failed to start server! ' + str(e))

    elif message.content == '!skyrim stop':
        print(message.content)
        try:
            ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
            await message.channel.send('Shutting down server!')
        except Exception as e:
            await message.channel.send('Failed to stop server! ' + str(e))

    elif message.content == '!skyrim status':
        try:
            print(message.content)
            instance = ec2_resource.Instance(instance_id)
            state = instance.state
            status = state.get('Name')
            await message.channel.send('Skyrim Together status: ' + status + '!')
        except Exception as e:
            await message.channel.send('Failed to fetch server status! ' + str(e))

    elif message.content == '!skyrim ip':
        print(message.content)
        try:
            instance = ec2_resource.Instance(instance_id)
            ip = instance.public_ip_address
            await message.channel.send('IP address: ' + ip + '!')
        except Exception as e:
            await message.channel.send('Failed to fetch IP address! ' + str(e))

client.run(discord_token)

