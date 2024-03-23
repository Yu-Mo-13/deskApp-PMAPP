import urllib3.request
import json

class Curl:
    def __init__(self, url):
        self.url = url

    def get(self):
        http = urllib3.PoolManager()
        r = http.request('GET', self.url)
        return json.loads(r.data.decode('utf-8'))
    
    def post(self, added_url):
        http = urllib3.PoolManager()
        r = http.request('POST', self.url + added_url)
        return json.loads(r.data.decode('utf-8'))
    
    def delete(self, added_url):
        http = urllib3.PoolManager()
        r = http.request('DELETE', self.url + 'delete' + added_url)
        return json.loads(r.data.decode('utf-8'))
    
    def deleteAll(self):
        http = urllib3.PoolManager()
        r = http.request('DELETE', self.url + 'delete/all')
        return json.loads(r.data.decode('utf-8'))
