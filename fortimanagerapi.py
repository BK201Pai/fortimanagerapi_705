import requests
import json

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # type: ignore

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
        query = {}
        params['url'] = url
        query['method'] = method
        query['params'] = [params]
        query['id'] = id
        query['session'] = self.tknSession
        req = self.s.post(self.url, json=query, verify=False)
        return req

    def getAllTask(self, params={}, id=1):
        req = self.generatePayloadRequest("get", "/task/task", params, id)
        app = json.loads(req.text)
        print(req.status_code)
        return app['result']

    def getTaskByID(self, TaskID, params={}, id=1):
        req = self.generatePayloadRequest("get", f"/task/task/{TaskID}", params, id)
        app = json.loads(req.text)
        return app['result']
