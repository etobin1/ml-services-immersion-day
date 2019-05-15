import boto3
import requests
import calendar
import time
import json
from requests_aws4auth import AWS4Auth


my_session = boto3.session.Session()
region = my_session.region_name
# region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

s3_client = boto3.resource('s3')
host = '' # Replace with the elasticsearch host name
s3_bucket = '' # Replace with your S3 bucket name

index = 'lambda-index'
type = 'lambda-type'
url = host + '/' + index + '/' + type + '/'

headers = { "Content-Type": "application/json" }

def lambda_handler(event, context):


    s3_object_key = event['Records'][0]['s3']['object']['key']
    s3_object = s3_client.Object(s3_bucket, s3_object_key)
    content = str(s3_object.get()['Body'].read().decode('utf-8'))
    my_str = content.replace("\'", "\"")
    json_object = json.loads(my_str)
    entities = json_object['Entities']

    i = 0
    for entity in entities:
        # Get the primary key for use as the Elasticsearch ID
        id = str(int(round(time.time() * 1000)))
        # Create a list of entities
        document = {}
        document['FileName'] = s3_object_key
        document['Type'] = entity['Type']
        document['Text'] = entity['Text']
        document['Score'] = entity['Score']
        i+=1
        print(document)
        r = requests.put(url + id, auth=awsauth, json=document, headers=headers)
        print(r.content)

    return str(i) + ' records processed.'
