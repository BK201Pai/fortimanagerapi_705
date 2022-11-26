import requests
import json

#ignore certificate
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class FortiManager:
    def __init__(self, ip, user, password):
        #FMG json-rpc wants all calls on the same url
        self.url = 'https://' + ip + '/jsonrpc'
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

    def generatePayloadRequest(self, method, url, params={}, id=1):
        payload = {"method": method, "params": [{"url": url, json.dumps(params)}], "id": id, "session": self.tknSession}
        req = self.s.post(self.url, json=payload, verify=False)
        return req

    def getAllTask(self, id=1, data={}):
        print(f"return status {req.status_code}")
        req = self.generatePayloadRequest("get", "/task/task", json.dumps(data), id)
        app = json.loads(req.text)
        return app['result']

    def getTaskByID(self, TaskID, id=1, data={}):
        req = self.generatePayloadRequest("get", f"/task/task/{TaskID}", data, id)
        app = json.loads(req.text)
        return app['result']
