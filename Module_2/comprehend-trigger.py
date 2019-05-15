import boto3
import json


s3 = boto3.client('s3')
comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
s3_bucket = ''

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def lambda_handler(event, context):

    s3_object_key = event['Records'][0]['s3']['object']['key']
    print(s3_object_key)
    s3_object = s3.get_object(Bucket=s3_bucket, Key=s3_object_key)
    content = s3_object['Body'].read()
    content_list = list(chunkstring(str(content), 5000))

    print(content_list)

    i=0
    for section in content_list:
        comprehend_response = comprehend.detect_entities(
            Text=str(section), LanguageCode='en'
        )

        # Create a temp file to upload to S3
        file_object = open('/tmp/workfile', 'w')
        file_object.write(str(comprehend_response))
        file_object.close()

        #Read the file object and write it to S3
        f = open('/tmp/workfile', 'r')
        body = f.read()
        processed_document = 'json/'+str(i)+'_'+s3_object_key
        print('processed document: '+ processed_document)
        response = s3.put_object(Bucket=s3_bucket, Key=processed_document, Body= body)
        i+=1
