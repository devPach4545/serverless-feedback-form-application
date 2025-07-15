# src/alert-publisher/app.py

import json
import os
import boto3

# Get the SNS topic ARN from an environment variable
TOPIC_ARN = os.environ['TOPIC_ARN']

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    """
    Formats a message and publishes it to the SNS topic for negative feedback.
    """
    print(f"Received event: {json.dumps(event)}")
    
    email = event.get('email')
    message = event.get('message')
    
    # Format the message for the email notification
    notification_subject = "Negative Feedback Alert"
    notification_message = (
        f"A new piece of negative feedback has been submitted.\n\n"
        f"From: {email}\n"
        f"Message: \"{message}\""
    )
    
    # Publish to the SNS topic
    sns_client.publish(
        TopicArn=TOPIC_ARN,
        Subject=notification_subject,
        Message=notification_message
    )
    
    print(f"Published alert to SNS topic: {TOPIC_ARN}")
    
    # Pass the original event through to the next step
    return event