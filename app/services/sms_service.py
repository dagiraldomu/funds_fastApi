from app.settings.config import settings
import boto3

# Create an SNS client
sns_client = boto3.client(
    'sns',
    region_name='us-east-1', # Replace with your region
    aws_access_key_id=settings.aws_access_key,
    aws_secret_access_key=settings.aws_secret_key
)

# Send an SMS message
def send_sms(phone_number, message):
    response = sns_client.publish(
        PhoneNumber='+57'+phone_number,
        Message=message,
    )
    return response
