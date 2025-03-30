import os
import json
import base64
from PIL import Image
import boto3
from botocore.exceptions import ClientError
from typing import Optional

# Load AWS credentials from environment variables
def get_aws_client(service_name: str, region_name: str = "us-east-1") -> boto3.client:
    """Initialize a boto3 client with credentials from environment variables."""
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in environment variables.")
    
    return boto3.client(
        service_name,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

# Function to encode image to base64
def encode_image_to_base64(image_path: str) -> str:
    """Convert an image file to base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        raise ValueError(f"Image file not found at: {image_path}")

# Function to invoke Bedrock model
def invoke_bedrock_model(image_base64: str, prompt: str, model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0") -> str:
    """Invoke the Bedrock model with an image and prompt."""
    bedrock = get_aws_client("bedrock-runtime")
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_base64
                        }
                    }
                ]
            }
        ],
        "max_tokens": 8000,
        "temperature": 0.0,
        "top_p": 0.0,
        "anthropic_version": "bedrock-2023-05-31"
    }

    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            body=json.dumps(payload)
        )
        output_binary = response["body"].read()
        output_json = json.loads(output_binary)
        return output_json["content"][0]["text"]
    except ClientError as e:
        raise Exception(f"Failed to invoke Bedrock model: {str(e)}")

# Main function to tie it all together
def identify_medical_equipment(image_path: str, prompt: str = "Name in the medical equipment in this picture in one short phrase. No other text allowed.") -> str:
    """Identify medical equipment in an image using Bedrock."""
    image_base64 = encode_image_to_base64(image_path)
    return invoke_bedrock_model(image_base64, prompt)

# Example usage
if __name__ == "__main__":
    # os.environ["AWS_ACCESS_KEY_ID"] = 
    # os.environ["AWS_SECRET_ACCESS_KEY"] = 

    image_path = r"C:\Users\14384\Desktop\test.jpeg"
    prompt = "Name the medical equipment in this picture in one short phrase. No other text allowed."
    
    try:
        result = identify_medical_equipment(image_path, prompt)
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")