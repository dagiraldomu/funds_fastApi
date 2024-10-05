from app.settings.config import settings
import boto3
from botocore.exceptions import ClientError


# Create an SNS client
ses_client = boto3.client(
    'ses',
    region_name='us-east-1', # Replace with your region
    aws_access_key_id=settings.aws_access_key,
    aws_secret_access_key=settings.aws_secret_key
)

def send_email(sender, recipient, subject, body_text, body_html):
    # The email body for recipients with non-HTML email clients
    body_text = body_text

    # The HTML body of the email
    body_html = body_html

    # Send the email
    try:
        response = ses_client.send_email(
            Source=sender,
            Destination={
                'ToAddresses': [recipient]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body_text
                    },
                    'Html': {
                        'Data': body_html
                    }
                }
            }
        )
    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")
    else:
        print(f"Email sent! Message ID: {response['MessageId']}")

