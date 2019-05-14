import boto3
import json

region = my_session.region_name

# region = 'us-east-1'
s3 = boto3.client('s3')
comprehend = boto3.client(service_name='comprehend', region_name='region')
s3_bucket = ''

def lambda_handler(event, context):
    if event['Records'][0]['eventName'] == 'ObjectCreated:Put':
        s3_object_key = event['Records'][0]['s3']['object']['key']
        s3_object = s3.get_object(Bucket=s3_bucket, Key=s3_object_key)
        content = s3_object['Body'].read()
    else:
        print('Error: Could not download object')

    comprehend_response = comprehend.detect_entities(
        Text=str(content)
    )

    # Create a temp file to upload to S3
    file_object = open('/tmp/workfile', 'w')
    file_object.write(comprehend_response)
    file_object.close()

    #Read the file object and write it to S3
    f = open('/tmp/workfile', 'r')
    body = f.read()
    processed_document = '/processed/'+document
    response = s3.put_object(Bucket=bucket, Key=processed_document, Body= body)
    return response
