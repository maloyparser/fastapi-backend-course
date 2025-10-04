import os
import requests
import json
from dotenv import load_dotenv
load_dotenv() 
GITHUB_API = 'https://api.github.com'
class GistStorage:
    def __init__(self, token: str = None, gist_id: str = None, filename: str = 'tasks.json'):
        self.token: str = token or os.getenv('GITHUB_TOKEN')
        self.gist_id: str = gist_id or os.getenv('GIST_ID')
        self.filename: str = filename
        if not self.token or not self.gist_id:
            raise RuntimeError('GITHUB_TOKEN and GIST_ID must be given')
        self.headers: dict = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github+json'
        }
        
    def _gist_url(self) -> str:
        return f'{GITHUB_API}/gists/{self.gist_id}'
    # loading task list from gist
    def load(self) -> list[dict]:
        r = requests.get(self._gist_url(), headers = self.headers, timeout = 10)
        r.raise_for_status()
        gist_data: dict = r.json()
        files: dict = gist_data.get('files', {})
        if self.filename not in files:
            return []
        content: str = files[self.filename]['content']
        try:
            data: dict = json.loads(content)
            return data.get('tasks', [])
        except json.JSONDecodeError:
            return []
    # saving task list on gist    
    def save(self, tasks: list[dict]) -> None:
        body: dict = {
            'files': {
                self.filename: {
                    'content': json.dumps({'tasks': tasks})
                }
            }
        }
        r = requests.patch(self._gist_url(), headers = self.headers, json = body, timeout = 10)
        r.raise_for_status()
