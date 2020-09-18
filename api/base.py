import configparser
import json
import os

import requests
from requests.auth import HTTPBasicAuth
import logging

logging.basicConfig(level=logging.DEBUG)


class Base:
    def __init__(self, **kwargs):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(__file__), '..', 'config', 'default.cfg'))
        self.s = requests.Session()
        self.s.auth = HTTPBasicAuth(self.config['api']['key'], '')
        self.urls = {
            'saved_searches': self.config['api']['host'] + 'data/v1/searches'
            }
        
    
    def post(self, **kwargs):
        return self.s.post(url=self.get_url(), json=self.data)

    def put(self, url):
        return self.s.put(url=url, json=self.data)

    def delete_by_id(self, url):
        return self.s.delete(url=url)
    
    def get_by_id(self, url):
        return self.s.get(url=url)
        