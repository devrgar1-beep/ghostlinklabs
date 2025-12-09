import json
import requests

def main(req):
    ghostlink_url = "https://api.ghostlink.ai"
    response = requests.post(f"{ghostlink_url}/analyze", json=req.get_json())
    return response.json()
