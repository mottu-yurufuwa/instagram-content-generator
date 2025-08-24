import requests
from dotenv import load_dotenv
import os

load_dotenv()

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

print(f"API Key exists: {bool(CLAUDE_API_KEY)}")
print(f"API Key length: {len(CLAUDE_API_KEY) if CLAUDE_API_KEY else 0}")

headers = {
    'Content-Type': 'application/json',
    'x-api-key': CLAUDE_API_KEY,
    'anthropic-version': '2023-06-01'
}

data = {
    'model': 'claude-3-sonnet-20240229',
    'max_tokens': 100,
    'messages': [{'role': 'user', 'content': 'Hello, test message'}]
}

try:
    response = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers=headers,
        json=data
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Text: {response.text}")
    
    if response.status_code == 200:
        print("API test successful!")
    else:
        print("API test failed!")
        
except Exception as e:
    print(f"Exception: {e}")