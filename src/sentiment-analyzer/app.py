# src/sentiment-analyzer/app.py

import json
import boto3

comprehend_client = boto3.client('comprehend')

def lambda_handler(event, context):
    """
    Receives the message from the Step Function, calls Comprehend to
    detect sentiment, and returns the original data plus the sentiment.
    """
    print(f"Received event: {json.dumps(event)}")
    
    message = event.get('message', '')
    
    # Call Comprehend to detect sentiment
    response = comprehend_client.detect_sentiment(
        Text=message,
        LanguageCode='en'
    )
    
    sentiment = response.get('Sentiment', 'UNKNOWN')
    print(f"Detected sentiment: {sentiment}")
    
    # Pass the original data along with the new sentiment
    event['sentiment'] = sentiment
    
    return event