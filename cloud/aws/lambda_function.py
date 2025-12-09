import json
import requests

def lambda_handler(event, context):
    ghostlink_url = "https://api.ghostlink.ai"
    response = requests.post(f"{ghostlink_url}/analyze", json=event)
    return response.json()
