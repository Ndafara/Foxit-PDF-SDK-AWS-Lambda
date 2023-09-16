import json
from FoxitPDFSDKPython3 import fsdk
from FoxitPDFSDKPython3 import *
import boto3


def lambda_handler(event, context):
    sn = "put_your_sn_number_here"
    key = "put_your_key_here"

    fsdk.Library_Initialize(sn, key)

    # s3 bucket and object details
    s3_bucket_name = "foxit-lambda-demo"
    s3_key = "lambda_doc.pdf"
    s3_updated_key = "lambda_doc_updated.pdf"

    # Download the original PDF from S3
    s3 = boto3.client('s3')
    original_pdf_filename = "/tmp/original.pdf"

    s3.download_file(s3_bucket_name, s3_key, original_pdf_filename)

    # Load the PDF
    document = fsdk.PDFDoc(original_pdf_filename)

    # Load the PDF
    error_code = document.Load("")

    if error_code != e_ErrSuccess:
        response = "Document was not loaded successfully"
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    # Get the first page of the PDF
    page = document.GetPage(0)
    page.StartParse(fsdk.PDFPage.e_ParsePageNormal, None, False)

    # Set the Style
    richtext_style = RichTextStyle()
    richtext_style.font = Font("Times New Roman", 0, Font.e_CharsetANSI, 0)
    richtext_style.text_color = 0x000000  # Black Color
    richtext_style.text_size = 10

    # Update the PDF with Text
    first_line = page.AddText("This line was added to the original PDF", RectF(1, 750, 200, 770), richtext_style)

    second_line = page.AddText("This is the second line added to the original PDF", RectF(1, 720, 200, 760),
                               richtext_style)

    # Generate the content on the PDF
    page.GenerateContent()

    # Save the PDF to a local temporary file
    pdf_filename_local = "/tmp/local_pdf.pdf"
    document.SaveAs(pdf_filename_local, fsdk.PDFDoc.e_SaveFlagIncremental)

    # Upload the Updated PDF to S3

    s3.upload_file(pdf_filename_local, s3_bucket_name, s3_updated_key)

    response = "Successfully updated PDF in S3 using the Foxit PDF SDK!'"

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
