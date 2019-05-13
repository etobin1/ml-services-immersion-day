# Module 3 - ElasticSearch indexing

In this module we'll be creating the indexing portion of the document image processing and indexing pipeline.  The services that we'll be interacting with are Amazon S3, Amazon ElasticSearch, and AWS Lambda.  

![ElasticSearch Architecture](elasticsearch-arch.png)

When a JSON document is uploaded to S3 under the `json/` object key prefix, Lambda will receive an event trigger.  The Lambda function will process the event, retrieve the document from S3 and submit it to ElasticSearch for indexing. Elasticsearch will respond with an HTTP response that indicates the successful receipt of the payload. The ElasticSearch index will provide entity based search and return a document that you can retrieve from your index for further review.

Follow the steps below to complete Module 3.

<details>
<summary><strong>1. Create an Amazon ElasticSearch Index(click to expand)</strong></summary><p>

</p></details>
<details>
<summary><strong>2. Create a Lambda Function(click to expand)</strong></summary><p>
1. Sign in to the [AWS Management Console](https://console.aws.amazon.com).

2. Navigate to Lambda by searching `Lambda` in the center search bar and clicking on `Lambda` in the results.

3. Click **Create Function**

4. Choose **Author From Scratch** and provide a function name that you can use to uniquely identify your function. Select **Python 3.6** as the runtime

5. Expand the section called **Choose or create an execution role**, select **Use existing role** and select **ElasticSearch-Demo** as the role and click **Create Function**

6. In the Lambda function, select **S3** from the Add Trigger list on the top left of the page.

7. Scroll down to configure the trigger in the **Configure triggers** section by selecting your bucket name from the drop down. Then, select **All object create events** for Event type. Next, select `json/` as the prefix, and leave the Suffix section blank.

8. Ensure that there is a checkmark in the box next to enable trigger, and click **Add**

9. Scroll up and click on your Lambda function's name in the designer, and then scroll down to your function's code.

10. Copy your code from the [es-upload-trigger.py](es-upload-trigger.py) function included here in the repo. Be sure to edit line 6 to include your S3 bucket name.

11. Click **Save**, at the top of the page.  
</p></details>
