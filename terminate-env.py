import boto3
def lambda_handler(event, context):
  account_client = boto3.client('sts')
  client = boto3.client('ec2')
  regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
  print(regions)
  for region in regions:

      client = boto3.client('elasticbeanstalk' , region_name= region)
      print("region is " +region)
      envs = client.describe_environments(
          MaxRecords=123

      )
      envlist=[]
      print('terminating these environments-')
      try:
          for env in envs['Environments']:
              if env['Status']!='Terminated' and env['Status']!= 'Terminating':
                  delete=True
                  env_arn=env['EnvironmentArn']
                  tags=client.list_tags_for_resource(ResourceArn=env_arn)['ResourceTags']
                  for tag in tags:
                      if( tag['Key'] =='AutoDelete' and tag ['Value'] == 'false'):
                          delete=False
                  print(env['EnvironmentName'])
                  if(delete==True):
                    print("will delelete this ")  
                    envlist.append(env['EnvironmentName'])

          print(envlist)
          for env in envlist:
              try:
                  response = client.terminate_environment(

                  EnvironmentName=env,
                  TerminateResources=True
                  )
              except Exception as e:
                print(e)    
      except Exception as e:
          print(e)
