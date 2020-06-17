import requests

API_URL = 'http://127.0.0.1:8000'
with open('t2.txt') as fp:
    content = fp.read()

response = requests.post(
    '{}/files/t2.txt'.format(API_URL), data=content
)
# curl -X POST -H "Content-Type: *.txt" --data-binary @ttt.txt 127.0.0.1:8000/files/ttt4.txt