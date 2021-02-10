import json
import boto3
import os

Commit_ID = "Commit_ID"
Commit_Message = "Commit_Message"
FullName = "Developed By DevOps Team"
UserName = "Git Username"
pname = os.environ.get('GitPullCodeBuild')
ECR_BASE_URI = os.environ.get('ECR_BASE_URI')
Branch_Name = os.environ.get('Branch_Name')
Config_File = os.environ.get('Config_File_Path')
Key = os.environ.get('SSH_Key_Path')

def handler(event, context):
  print('EVENT >>>>>>>>>', event, '\n')
  body = json.loads(event['body'])
  GitUrl = body ['project']['git_ssh_url']
  Repository_Name = body ['repository']['name']
  Gitlab_Branch_Name = body ['ref'].replace('refs/heads/', '').replace('refs/tags/', 'tags/')
  Commit_Details = body ['commits']
  global UserName, FullName
  FullName = body['user_name']
  UserName = body['user_username']

  for res in body ['commits']:
    global Commit_ID, Commit_Message
    Commit_ID = res.get('id')
    Commit_Message = res.get('message')

  print(Repository_Name, '->', Gitlab_Branch_Name, '->', Commit_Message, '->', Commit_ID, '->', FullName, '->', UserName)

  if Branch_Name == Gitlab_Branch_Name:
    codebuild_client = boto3.client('codebuild')
    new_build = codebuild_client.start_build(projectName=pname, environmentVariablesOverride=[
      {
        'name': 'GitUrl',
        'value': GitUrl,
        'type': 'PLAINTEXT'
      },
      {
        'name': 'Branch_Name',
        'value': Branch_Name,
        'type': 'PLAINTEXT'
      },
      {
        'name': 'Full_Name',
        'value': FullName,
        'type': 'PLAINTEXT'
      },
      {
        'name': 'Commit_SHA',
        'value': Commit_ID,
        'type': 'PLAINTEXT'
      },
      {
        'name': 'Commit_Message',
        'value': Commit_Message,
        'type': 'PLAINTEXT'
      },
      {
        'name': 'ECR_BASE_URI',
        'value': ECR_BASE_URI,
        'type': 'PLAINTEXT'
      }
    ])
    return {
      'statusCode': 200,
      'body': json.dumps(pname +' Codebuild Execution has Started...')
    }
  else:
    print (Gitlab_Branch_Name +" Branch is not configured with webhooks... \n")
    return {
      'statusCode': 200,
      'body': json.dumps(Gitlab_Branch_Name +' Branch is not configured with webhooks...')
    }
  print('Execution Completed.\n')
