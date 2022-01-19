# extract-paragraphs-with-aws-textract
Since AWS Textract does not have a native function to extract paragraphs, this repository provides a set of ad hoc functions in Python 3.X. built on top of the AWS Python SDK (boto3) to extract paragraphs from AWS Textract responses.

PLEASE NOTE THAT:

1. It is assumed that your client has the neccesary IAM permissions to access the recquired resources
2. Since AWS Textract analyze PDF files by running asynchronous operations, the current version assumes that you've already created an s3 bucket and that the PDF files are already stored there. 

UPCOMING FEATURES:

- Address abstract cases with the paragrpah constructor function. 
- Create a bucket
- Upload pdf files from local directory
- Export data in different formats

Please feel free to suggest new features or improvents to the current code.
