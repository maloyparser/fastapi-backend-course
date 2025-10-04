import os
import requests
from dotenv import load_dotenv
load_dotenv()
class Cloudflare:
    def __init__(self, api_key: str = None, acc_id: str = None):
        self.api_key = api_key or os.getenv("CLOUDFLARE_API_KEY")
        self.acc_id = acc_id or os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.url = f"https://api.cloudflare.com/client/v4/accounts/{self.acc_id}/ai/run/@cf/meta/llama-3-8b-instruct"
        
    def get_llm_response(self, text:str) -> str:
        headers = {
            "Authorization": f'Bearer {self.api_key}',
            "Content-type": "application/json"
        }
        pyload = {
            'messages': [
                {'role': 'system', 'content': 'I will help you with somethimg'},
                {'role': 'user', 'content': text}
            ]
        }

        response = requests.post(self.url, headers=headers, json=pyload, timeout=15)
        print("CLOUDFLARE RAW RESPONSE:")
        print(response.text)
        try:
            data = response.json()
            return data['result']['response']
        except (KeyError, IndexError):
            return 'Error: wrong API answer'