import json
from FoxitPDFSDKPython3 import fsdk
from FoxitPDFSDKPython3 import *
import boto3
from datetime import date


def lambda_handler(event, context):
    sn = "put_your_sn_number_here"
    key = "put_your_key_here"

    fsdk.Library_Initialize(sn, key)

    # Get the date
    today = date.today()

    # S3 bucket and object details
    s3_bucket_name = "foxit-lambda-demo"
    s3_template_key = "Daily Sales Template.pdf"
    s3_sales_data_key = "sales_data.json"
    s3_sales_report_key = f"Sales_Reports/{today}.pdf"

    # Download the PDF template from S3
    s3 = boto3.client('s3')
    pdf_filename_template = "/tmp/template.pdf"

    s3.download_file(s3_bucket_name, s3_template_key, pdf_filename_template)

    # Load the PDF template
    document = fsdk.PDFDoc(pdf_filename_template)

    # Load the PDF
    error_code = document.Load("")

    if error_code != e_ErrSuccess:
        response = "Template was not loaded successfully"
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    # Get the first page of the PDF
    page = document.GetPage(0)
    page.StartParse(fsdk.PDFPage.e_ParsePageNormal, None, False)

    # Set the style
    richtext_style = RichTextStyle()
    richtext_style.font = Font("Times New Roman", 0, Font.e_CharsetANSI, 0)
    richtext_style.text_color = 0x000000  # Black color
    richtext_style.text_size = 15

    # Process the sales data from the JSON file
    total_sales = 0
    products = []

    try:
        # Fetch the sales data
        response = s3.get_object(Bucket = s3_bucket_name, Key = s3_sales_data_key)

        # Deserialize the file's contents
        contents = response['Body'].read().decode()

        # Parse the contents into a dictionary
        sales_data = json.loads(contents)
        print(sales_data)

        sales = sales_data['sales']
        for record in sales:
            total_sales += record['total_amount']
            products.append(record['product'])
    except Exception as e:
        print(e)

    # Update the PDF with the data

    # Add date to the report
    date_line = page.AddText(f"Date: {today}", RectF(1, 600, 350, 620), richtext_style)

    # Add products sold
    products_sold = page.AddText(f"Products Sold: {products}", RectF(1, 520, 400, 605), richtext_style)

    # Add total sales
    all_sales = page.AddText(f"The total sales were: {total_sales}", RectF(1, 490, 350, 590), richtext_style)

    # Generate the content of the PDF
    page.GenerateContent()

    # Save the PDF to a local temporary file
    pdf_filename_local = "/tmp/generated_sales_report.pdf"
    document.SaveAs(pdf_filename_local, fsdk.PDFDoc.e_SaveFlagIncremental)

    s3.upload_file(pdf_filename_local, s3_bucket_name, s3_sales_report_key)

    response = "Successfully generated a PDF Sales Report in S3 using the Foxit PDF SDK!"

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
