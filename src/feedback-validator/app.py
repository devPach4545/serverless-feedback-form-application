# src/feedback-validator/app.py

import json
import os
import boto3
import uuid

# Get the Step Function ARN from an environment variable
STATE_MACHINE_ARN = os.environ['StepFunctionArn']

# Create a Step Functions client
sfn_client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    """
    Receives the API Gateway event, validates the input, and starts the
    Step Function execution.
    """
    print(f"Received event: {json.dumps(event)}")

    try:
        # The body of a POST request from a REST API is a JSON string
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        message = body.get('message')

        # Basic validation
        if not email or not message:
            print("Validation failed: Email or message is missing.")
            return {
                "statusCode": 400,
                "headers": { "Access-Control-Allow-Origin": "*" },
                "body": json.dumps({"error": "Email and message are required."})
            }

        # Create a unique ID for this feedback entry
        feedback_id = str(uuid.uuid4())
        
        # This is the input that will be passed to our state machine
        state_machine_input = {
            "id": feedback_id,
            "email": email,
            "message": message
        }

        # Start the Step Function execution
        response = sfn_client.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            input=json.dumps(state_machine_input)
        )
        
        print(f"Started state machine execution: {response['executionArn']}")
        
        return {
            "statusCode": 202, # 202 Accepted
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": json.dumps({"message": "Feedback received and is being processed."})
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": json.dumps({"error": "Invalid JSON in request body."})
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            "statusCode": 500,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": json.dumps({"error": "Internal server error."})
        }