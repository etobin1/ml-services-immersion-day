import boto3

def lambda_handler(event, context):

    #insert your bucket name here
    bucket = ""
    document = event['Records'][0]['s3']['object']['key']

    # Detect text in the document
    s3 = boto3.client('s3')
    client = boto3.client('textract')

    #process the file using S3 object
    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}})

    #Get the text blocks
    blocks=response['Blocks']
    print ('Detected Document Text')

    # Create a temp file to upload to S3
    file_object = open('/tmp/workfile', 'w')
    for block in blocks:
        if block['BlockType'] == 'LINE':
            file_object.write(block['Text']+'\n')
    file_object.close()

    #Read the file object and write it to S3
    f = open('/tmp/workfile', 'r')
    body = f.read()
    processed_document = '/processed/'+document
    response = s3.put_object(Bucket=bucket, Key=processed_document, Body= body)
    return response
