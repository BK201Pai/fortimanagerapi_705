import requests
import json
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # type: ignore

class FortiManager:
    def __init__(self, ip: str, user: str, password: str):
        #FMG json-rpc wants all calls on the same url
        self.url = 'https://' + ip + '/jsonrpc'
        self.s = requests.Session()
        #Static payload login as it is always the same
        payload = {"id": 1, "method": "exec","params": [{"data": {"user": user,"password": password},"url": "/sys/login/user"}]}
        self.r = self.s.post(self.url, json=payload, verify=False)
        print(f"login status {self.r.status_code}")
        appSession = json.loads(self.r.text)
        self.tknSession = appSession['session']
        
    #Static payload logout as it is always the same
    def logout(self):
        payload = {"id": 1, "method": "exec","params": [{"url": "/sys/logout"}], "session": self.tknSession}
        req = self.s.post(self.url, json=payload, verify=False)
        return req.status_code

    #Since FMG wants all requests on the same url with post as per json-rpc standard,
    #the method and the url is specified in the request json body.
    #params is a dict for additional filters or fields used by the query, url is contained inside of params.
    #params has key and values described in the api documentation .
    #documentation for apis is available at fndn.fortinet.net
    def generatePayloadRequest(self, method: str, url: str, params: dict={}, id: int=1):
        query = {}
        params['url'] = url
        query['method'] = method
        query['params'] = [params]
        query['id'] = id
        query['session'] = self.tknSession
        req = self.s.post(self.url, json=query, verify=False)
        return req

    #Since the json-rpc standard incapsulates the result in a json along with the id and the method, all requests will return only the 'result' field
    
    #Returns all tasks (or last 10.000) present in the Task Monitor section
    def getAllTasks(self, params: dict={}, id: int=1):
        req = self.generatePayloadRequest("get", "/task/task", params, id)
        app = json.loads(req.text)
        print(req.status_code)
        return app['result']

    #Returns a chosen Task present in the Task Monitor section using the ID
    def getTaskByID(self, TaskID: int, params: dict={}, id: int=1):
        req = self.generatePayloadRequest("get", f"/task/task/{TaskID}", params, id)
        app = json.loads(req.text)
        return app['result']

    #Returns action lines executed from the task
    def getTaskLine(self, TaskID: int, params: dict={}, id: int=1):
        req = self.generatePayloadRequest("get", f"/task/task/{TaskID}/line", params, id)
        app = json.loads(req.text)
        return app['result']

    #Returns all devices connected
    def getAllDevices(self, params: dict={}, id: int=1):
        req = self.generatePayloadRequest("get", "/dvmdb/device", params, id)
        app = json.loads(req.text)
        return app['result']

    #Sets a param for selected device
    #All settings to change must be inside the data dict
    #name is the name of the device
    def setDeviceParam(self, name: str, data: dict={}, id: int=1):
        params = {}
        data['name'] = name
        params['data'] = [data]
        req = self.generatePayloadRequest("set", "/dvmdb/device", params, id)
        app = json.loads(req.text)
        return app['result']
