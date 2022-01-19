import os
import boto3

#AWS CLI MUST BE ALREADY CONFIGURED
textract_client = boto3.client('textract')

# NOT A GOOD PRACTICE, BUT YOU CAN USE THE FOLLOWING PARAMEMTERS TO AUTHENTICATE YOUR BOTO3 CLIENT
# boto3.client('textract', aws_access_key_id='', aws_secret_access_key='', region_name='')
                              

def extract_data_from_response(response):
    
    """
    Expects an AWS Textract response with NextTokens. 
    """
    
    data = []
    get_data = response
    if get_data['JobStatus'] == 'SUCCEEDED':
        while 'NextToken' in get_data:
            data.append(get_data)
            get_data = textract_client.get_document_text_detection(
                JobId=job_id,
                NextToken=get_data['NextToken']
            )
            
    return data

def group_lines_by_page(data):
    
    """
    Expects a list of AWS Textract Responses
    """

    data = data
    number_of_pages = response['DocumentMetadata']['Pages']
    pages = [{'PAGE_NUMBER':i, 'LINES':[]} for i in range(1, number_of_pages + 1)]
    
    for i in pages:
        for k in data:
            for l in k['Blocks']:
                if (l['BlockType'] == 'LINE') and (l['Page'] == i['PAGE_NUMBER']):
                    i['LINES'].append(l)

    return pages

def sort_lines_by_page(pages_obj):
    
    """
    Expects a Pages Object (LIST OF DICTS) with the following Keys:
    
        - PAGE_NUMBER: int
        - LINES: list of dicts from AWS Textract BlockType Line
    """
    
    pages = pages_obj
    
    pairs = []

    for i in pages:

        pairs_to_sort = {}

        for k in i['LINES']:

            ID = k['Id']
            TOP = k['Geometry']['BoundingBox']['Top']
            pairs_to_sort[ID] = TOP

        pairs_to_sort = dict(pairs_to_sort)
        sorted_pairs = {k: v for k, v in sorted(dict(pairs_to_sort).items(), key=lambda x: x[1])}
        pairs.append(sorted_pairs)

    pages_with_sorted_lines = []   

    for i, n in enumerate(pairs):
        sorted_lines = []
        for key, value in n.items():
            for p in pages:
                for l in p['LINES']:
                    if l['Id'] == key:
                        sorted_lines.append(l)

        pages_with_sorted_lines.append(sorted_lines) 

    return pages_with_sorted_lines

def paragraph_constructor(sorted_pages_and_lines_object, file_name, remove_txt_file=True):

    """
    Expects a sorted_lines_by_page object. 
    """
    
    pages = sorted_pages_and_lines_object
    
    file_name = file_name
    file_name = file_name.split('.')
    file_name = file_name[0]

    with open(f'{file_name}.txt', 'w+') as f:
        for i in sorted_pgs_and_lines:
            for l in range(len(i)):        
                if l + 1 == len(i):
                    break
                else:
                    p_sub_zero = i[l]['Geometry']['BoundingBox']['Top']
                    p_plus_one = i[l+1]['Geometry']['BoundingBox']['Top']

                    if (p_plus_one - p_sub_zero) > 0.021 and (p_plus_one - p_sub_zero) < 0.03:
                        f.write(f"\n{i[l]['Text']}")
                    else:
                        f.write(f"\n{i[l]['Text']}")
                        f.write('\n------------------')
        f.close()
        
    #The paragraph split is given by a string full of '-' of len 19
    
    with open(f'{file_name}.txt') as f:
        lines = f.readlines()
        list_of_paragraphs = []
        paragraphs = []
        for l in lines:
            if l[0] == '-' and len(l) == 19:
                paragraph = " ".join(paragraphs)
                list_of_paragraphs.append(paragraph)
                paragraphs = []
            elif l == '-\n':
                pass
            else:
                l = l.replace('\n', '')
                if l in ['.', '-', ':', '']:
                    pass
                else:
                    paragraphs.append(l)
        
        f.close()
        
        if remove_txt_file:
            os.remove(f'{file_name}.txt')
    
    return list_of_paragraphs


#PROPOSED IMPLEMENTATION

BUCKET_NAME = ''
FILE_NAME = ''

start_text_extraction = textract_client.start_document_text_detection(
    DocumentLocation={
        'S3Object': {
            'Bucket': BUCKET_NAME,
            'Name': FILE_NAME
        }
    }
)

job_id = start_text_extraction['JobId']

response = textract_client.get_document_text_detection(JobId=job_id)
while response['JobStatus'] == 'IN_PROGRESS':
    response = textract_client.get_document_text_detection(JobId=job_id)

data = extract_data_from_response(response)
pages = group_lines_by_page(data)
sorted_pgs_and_lines = sort_lines_by_page(pages)
paragraphs = paragraph_constructor(sorted_pgs_and_lines, FILE_NAME)