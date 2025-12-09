import json
import requests

def ghostlink_handler(request):
    ghostlink_url = "https://api.ghostlink.ai"
    response = requests.post(f"{ghostlink_url}/analyze", json=request.get_json())
    return response.json()
