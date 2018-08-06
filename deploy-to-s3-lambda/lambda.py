from __future__ import print_function

import json
import boto3
import zipfile
import tempfile
import botocore
import traceback
import subprocess

print('Loading function')

cf = boto3.client('cloudformation')
code_pipeline = boto3.client('codepipeline')
s3 = boto3.client('s3')

def find_artifact(artifacts, name):
  for artifact in artifacts:
    if artifact['name'] == name:
      return artifact

  raise Exception('Input artifact named "{0}" not found in event'.format(name))

def get_artifact(from_bucket, from_key, dest_dir):
  with tempfile.NamedTemporaryFile() as tmp_file:
    s3.download_file(from_bucket, from_key, tmp_file.name)
    with zipfile.ZipFile(tmp_file.name, 'r') as zip:
      zip.extractall(dest_dir)

def upload_artifact(source_dir, to_bucket):
  command = ['./aws', 's3', 'sync', '--delete',
    source_dir + '/', 's3://' + to_bucket + '/']
  print(command)
  print(subprocess.check_output(command, stderr=subprocess.STDOUT))

def upload_configuration(config, to_bucket, to_key):
  print(config)
  with tempfile.NamedTemporaryFile('w+r+b') as outfile:
    outfile.write('var _gConf = ')
    json.dump(config, outfile)
    outfile.write(';')
    outfile.seek(0)
    s3.upload_fileobj(outfile, to_bucket, to_key)

def put_job_success(job, message):
  print('Putting job success')
  print(message)
  code_pipeline.put_job_success_result(jobId=job)

def put_job_failure(job, message):
  print('Putting job failure')
  print(message)
  code_pipeline.put_job_failure_result(jobId=job, failureDetails={
    'message': message, 'type': 'JobFailed'
  })

def get_user_params(job_data):
  try:
    # Get the user parameters which contain the stack, artifact and file settings
    user_parameters = job_data['actionConfiguration']['configuration']['UserParameters']
    decoded_parameters = json.loads(user_parameters)
  except Exception as e:
    # We're expecting the user parameters to be encoded as JSON
    raise Exception('UserParameters could not be decoded as JSON')
  return decoded_parameters

def lambda_handler(event, context):
  try:
    # Extract the Job ID
    job_id = event['CodePipeline.job']['id']

    # Extract the Job Data
    job_data = event['CodePipeline.job']['data']

    # Extract the params
    params = get_user_params(job_data)

    # Get the list of artifacts passed to the function
    artifacts = job_data['inputArtifacts']

    # Get the artifact details
    artifact = find_artifact(artifacts, 'FrontEnd')
    # Get artifact with
    from_bucket = artifact['location']['s3Location']['bucketName']
    from_key = artifact['location']['s3Location']['objectKey']
    artifact_dir = tempfile.mkdtemp()
    get_artifact(from_bucket, from_key, artifact_dir)
    # Upload
    upload_artifact(artifact_dir, params['bucket'])
    # Upload Configuration
    upload_configuration(params['config'], params['bucket'], 'app.config.js')

    put_job_success(job_id, 'Stack update complete')
  except Exception as e:
    # If any other exceptions which we didn't expect are raised
    # then fail the job and log the exception message.
    print('Function failed due to exception.')
    print(e)
    traceback.print_exc()
    put_job_failure(job_id, 'Function exception: ' + str(e))

  print('Function complete.')
  return "Complete."
