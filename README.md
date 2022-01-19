# extract-paragraphs-with-aws-textract
Since AWS Textract (the AWS OCR service) does not have a native function to extract paragraphs, this repository provides a set of Python 3.X functions built on top of the AWS Python SDK (boto3) to extract paragraphs from AWS Textract responses.

PLEASE NOTE THAT:

1. It is assumed that your client has the neccesary IAM permissions to access the different AWS resources required.
2. Since AWS Textract analyze PDF files by running asynchronous operations, the current version assumes that you've already created an s3 bucket and that the PDF files are already stored there. If not, please go to the boto3 docs to know how to create a bucket as well as upload files.
3. The paragraph_constructor is an ad hoc function for my use case. You may have to adapt it based on the space between lines in your data.

UPCOMING FEATURES:

- Address abstract cases with the paragrpah_constructor function. 
- Export data in different formats.
- AWS Cloudformation template for a serverless architecture to execute the functions.
Please feel free to suggest new features or improvements to the current code.
