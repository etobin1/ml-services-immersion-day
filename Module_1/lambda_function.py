import boto3
import json
import sys
import time


textract = boto3.client('textract')
s3 = boto3.client('s3')

bucket = '' #update this string with your bucket name

def lambda_handler(event, context):

    document = event['Records'][0]['s3']['object']['key']
    file_object = open('/tmp/workfile', 'w')

    def ProcessDocument(document):
        jobFound = False
        validType=False

        response = textract.start_document_text_detection(DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': document}})
        print('Processing type: Detection')
        print(str(response))
        validType=True
        jobId = response['JobId']
        wait(jobId)
        print('Start Job Id: ' + response['JobId'])

    def wait(jobId):
        response = textract.get_document_text_detection(JobId=jobId)
        jobStatus = response['JobStatus']
        if jobStatus == 'SUCCEEDED':
            print("Job SUCCEEDED, processing...")
            GetResults(jobId)
        else:
            print(str(response))
            time.sleep(10)
            wait(jobId)

    #Display information about a block
    def WriteBlockInfo(block):

        blocks=block['Blocks']
        print ('Detected Document Text')

        # Create a temp file to upload to S3
        for block in blocks:
            if block['BlockType'] == 'LINE':
                file_object.write(block['Text']+'\n')

    def GetResults(jobId):
        maxResults = 1000
        paginationToken = None
        finished = False

        while finished == False:

            response=None

            if paginationToken==None:
                response = textract.get_document_text_detection(JobId=jobId,
                    MaxResults=maxResults)
                WriteBlockInfo(response)
            else:
                response = textract.get_document_text_detection(JobId=jobId,
                    MaxResults=maxResults,
                    NextToken=paginationToken)
                WriteBlockInfo(response)

            blocks=response['Blocks']
            print ('Detected Document Text')
            print ('Pages: {}'.format(response['DocumentMetadata']['Pages']))

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

    s3_object_key = event['Records'][0]['s3']['object']['key']
    ProcessDocument(s3_object_key)
    file_object.close()

    #Read the file object and write it to S3
    f = open('/tmp/workfile', 'r')
    body = f.read()
    processed_document = 'processed/' + document
    response = s3.put_object(Bucket=bucket, Key=processed_document, Body= body)
    return response
