import urllib3.request
import json

class Curl:
    def __init__(self, url):
        self.url = url

    def get(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.url)
        return json.loads(r.data.decode('utf-8'))
    
    def post(self, data, added_url):
        http = urllib3.PoolManager()
        r = http.request('POST', self.url + added_url, fields=data)
        return json.loads(r.data.decode('utf-8'))
