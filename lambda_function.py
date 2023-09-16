from FoxitPDFSDKPython3 import fsdk
import json

def lambda_handler(event, context):

    sn = "put_your_sn_number_here"
    key = "put_your_key_here"

    fsdk.Library_Initialize(sn, key)

    # Create a new document
    document = fsdk.PDFDoc()

    # Create a new page
    page = document.InsertPage(-1, 595, 842)

    response = "Successfully created PDF from Lambda to s3 using Foxit!'"

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
