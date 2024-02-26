import requests

x = requests.get('http://127.0.0.1:5000/')
print(x.content)
print(x.status_code)