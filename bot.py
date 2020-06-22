#import sys
import time
import requests
import json

from config import COOKIE_BHA, COOKIE_NIKKI

url = "http://www.hi5.com/api/?application_id=user&format=JSON"

newValue = 0

def alert_payload():
    payload_ = {'method': 'tagged.header.renderAlerts',
                'api_signature': '',
                'track': '6TVYmoeLnp'}
    return payload_

def payload(userid_to_buy, price=0):
    payload_ = {'method': 'tagged.apps.pets.buyPetAsync',
                'api_signature': '',
                'track': 'xc7pz7WBpc',
                'userid_to_buy': str(userid_to_buy),
                'displayed_owner_id': '5415803446',
                'purchase_token': '',
                'ect': '0',
                'page_type': 'buyback',
                'pet_price': price,
                'one_click': '0',
                'source': 'web'}
    return payload_


files = [

]


def get_headers(cookie):
    headers = {
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://www.hi5.com',
        'DNT': '1',
        'Referer': 'http://www.hi5.com/apps/pets.html?dataSource=Pets&ll=nav',
        'Cookie': cookie
    }
    return headers

racerCount=0
def check_response(response):
    global newValue
    global racerCount

    if response['stat'] == 'ok':
        if response['results']['boughtPetOk']==True:
            racerCount -= 1
            return 0
        elif response['results']['petruninfo']['racerCount']>0:
            time.sleep(response['results']['petruninfo']['timeRemaining']/1000)
            racerCount+=1
            return 0
        elif response['results']['petruninfo']['racerCount'] < 4:
            time.sleep(response['results']['petruninfo']['timeRemaining'] / 1000)
            return 0

    if response['error']['code'] == 105:  # different price return price
        newValue = response['error']['newValue']
        # if len(str(newValue)) < 60:
        return 1

    if response['error']['code'] == 121:  # different price return price
        newValue = response['error']['pets'][0]['value']
        # if len(str(newValue)) < 60:
        return 0

    return 0


# 6118592912


def payload_generator(cookie, uid):
    analysis = 0
    for idx in range(uid, uid + 1):
        payload_new = payload(idx, newValue)
        response = requests.request("POST", url, headers=get_headers(cookie), data=payload_new, files=files)
        dict_response = json.loads(str(response.text))
        analysis = check_response(dict_response)

        if analysis == 1:
            payload_new = payload(idx, newValue)
            response = requests.request("POST", url, headers=get_headers(cookie), data=payload_new, files=files)
            dict_response = json.loads(str(response.text))
            analysis = check_response(dict_response)

        print(response.text)
    return analysis


def buy_two_way():
    x = 0
    print("Bha")
    x += payload_generator(COOKIE_BHA, 6119757178)
    print("Nikki")
    x += payload_generator(COOKIE_NIKKI, 6119757178)
    return x


for n in range(10000):
    p = buy_two_way()
    if racerCount<-1000:
        break

# payload_generator(cookie2)
