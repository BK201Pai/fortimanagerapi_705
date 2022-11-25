import requests
import json

#ignore certificate
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class FortiManager:
    def __init__(self, ip, user, password):
        ipaddr = 'https://' + ip
        #FMG json-rpc wants all calls on the same url
        self.url = ipaddr + '/jsonrpc'
        self.s = requests.Session()
        payload = {"id": 1, "method": "exec","params": [{"data": {"user": user,"password": password},"url": "/sys/login/user"}]}
        self.r = self.s.post(self.url, json=payload, verify=False)
        print(f"login status {self.r.status_code}")
        appSession = json.loads(self.r.text)
        self.tknSession = appSession['session']
    
    def logout(self):
        payload = {"id": 1, "method": "exec","params": [{"url": "/sys/logout"}], "session": self.tknSession}
        req = self.s.post(self.url, json=payload, verify=False)
        return req.status_code

    def generatePayloadRequest(self, method, url, data, id=1):
        payload = {"method": method, "params": [{"url": url, "data": {data}}], "id": id, "session": self.tknSession}
        req = self.s.post(self.url, json=payload, verify=False)
        return req

    def getAllTask(self, id=1, data={}):
        req = self.generatePayloadRequest("get", "/task/task", data, id)
        print(f"return status {req.status_code}")
        app = json.loads(req.text)
        return app['data']

    def getTaskByID(self, id=1, data={}):
        req = self.generatePayloadRequest("get", f"/task/task/{id}", data, id)
        print(f"return status {req.status_code}")
        app = json.loads(req.text)
        return app['data']
