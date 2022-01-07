import requests
from requests.auth import HTTPBasicAuth
import os
import json

from core.defaults import *

__all__ = ['UKGApi',]

class UKGApi:

    module = 'configuration'
    method = 'company-details'
    version = 'v1'

    def __init__(self):
        self.auth = HTTPBasicAuth(UKGUID, UKGPWD)
        self.headers = {'US-Customer-Api-Key': ClientAccessKey}
        self.base_url = os.getenv('RESTURLBASE')
        self.resp = 'No request made'


    def test_connection(self):
        response = self._get_request(self.module, self.method)
        return response.status_code == 200


    def _base_request(self, module, method, version, data, *args, **kwargs):
        if data:
            data = json.dumps(data)
        url = f'{self.base_url}{module}/{version}/{method}'
        base = {'url': url, 'data': data}
        return base


    def _get_request(self, module, method, version='v1', *args, **params):
        base = self._base_request(module, method, version, *args, **params)
        return requests.get(url=base['url'], auth=self.auth, headers=self.headers, params=base['data'])


    def get(self, *args, **kwargs):
        self.resp = self._get_request(self.module, self.method, self.version, *args, **kwargs)
        return self


    def _post_request(self, module, method, version='v1', params=None, *args, **kwargs):
        base = self._base_request(module, method, version, params, *args, **kwargs)
        return requests.post(url=base['url'], auth=self.auth, headers=self.headers, params=base['data'])


    def post(self, *args, **kwargs):
        self.resp = self._post_request(self.module, self.method, self.version, *args, **kwargs)
        return self
    

    def data(self):
        try:
            data = json.loads(self.resp.text)
            return data
        except AttributeError:
            print('No request was made')

