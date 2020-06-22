import json
import time

import requests

from config import COOKIE_BHA


def build_payload(payload, **kwargs):
    for key, value in kwargs.items():
        payload[key] = value
    return payload


class cash_run:
    url = "http://www.hi5.com/api/?application_id=user&format=JSON"
    payload_ = {
        'method': '',
        'api_signature': '',
        'track': 'xc7pz7WBpc',
    }
    METHODS = {
        'getUnfinishedRuns': 'tagged.apps.pets.cashruns.getUnfinishedRuns',
        'joinRoom': 'tagged.apps.pets.cashruns.joinRoom',
        'bid': 'tagged.apps.pets.cashruns.bid',
    }

    headers = {
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://www.hi5.com',
        'DNT': '1',
        'Referer': 'http://www.hi5.com/apps/pets.html?dataSource=Pets&ll=nav',
        'Cookie': ''
    }

    METHOD = 'method'
    GET_UNFINISHED_RUNS = 'getUnfinishedRuns'
    JOIN_ROOM = 'joinRoom'
    BID = 'bid'
    COOKIE = 'Cookie'

    def __init__(self, cookie, room_id=-1):
        self._get_unfinished_runs(cookie)
        self._join_room(cookie, room_id)
        self.cookie = cookie

    def get_headers(self, cookie):
        self.headers[self.COOKIE] = cookie
        return self.headers

    def _get_unfinished_runs(self, cookie):
        payload = build_payload(payload=self.payload_.copy(), METHOD=self.METHODS[self.GET_UNFINISHED_RUNS])
        print(payload)
        response = requests.request("POST", self.url, headers=self.get_headers(cookie), data=payload, files=[])
        print(response.text)

    def _join_room(self, cookie, room_id):
        payload = build_payload(payload=self.payload_.copy(), method=self.METHODS[self.JOIN_ROOM], room_id=room_id)
        print(payload)
        response = requests.request("POST", self.url, headers=self.get_headers(cookie), data=payload, files=[])
        self._assign_price(response)
        print(response.text)

    def _assign_price(self, resp):
        dict_response = json.loads(str(resp.text))
        self.price = dict_response['result']['room']['cashrun']['price']
        self.cashrun_id = dict_response['result']['room']['cashrun']['id']

    def bid(self):
        payload = build_payload(payload=self.payload_.copy(), method=self.METHODS[self.BID], cashrun_id=self.cashrun_id,
                                price=self.price)
        print(payload)
        response = requests.request("POST", self.url, headers=self.get_headers(self.cookie), data=payload, files=[])
        self.price = int(float(self.price) * 1.1)
        cash_run._wait_time(response)
        print(response.text)

    @staticmethod
    def _wait_time(resp):
        dict_response = json.loads(str(resp.text))
        time.sleep(dict_response['result']['timeRemaining'] / 1000)


c = cash_run(COOKIE_BHA)
for i in range(10):
    c.bid()
