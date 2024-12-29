import json
import requests


url = 'http://127.0.0.1:8100/joker/stream'
params = {
    "input": {"text": "xxx"},
}
headers = {"Content-Type": "application/json"}
response = requests.post(url, headers=headers, json=params)
print(response.text)