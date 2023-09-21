from FoxitPDFSDKPython3 import fsdk
import json
import boto3

def lambda_handler(event, context):

    sn = "put_your_sn_number_here"
    key = "put_your_key_here"

    fsdk.Library_Initialize(sn, key)

    # Create a new document
    document = fsdk.PDFDoc()

    # Create a new page
    page = document.InsertPage(-1, 595, 842)
    
    # Create the PDF in Lambda temporary folder
    pdf_filename = "/tmp/lambda_doc.pdf"
    document.SaveAs(pdf_filename, fsdk.PDFDoc.e_SaveFlagNoOriginal)
    
    # Upload the PDF to S3
    s3_bucket_name = "foxit-lambda-demo"
    s3_key = "lambda_doc.pdf"

    s3 = boto3.client("s3")
    s3.upload_file(pdf_filename, s3_bucket_name, s3_key)

    response = "Successfully created PDF from Lambda to S3 using the Foxit PDF SDK!'"

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
