#!/usr/bin/env python3
# encoding: utf-8

import json
import requests

import time
import hmac
import hashlib
import base64
import urllib.parse

def addTag():
    timestamp = str(round(time.time() * 1000))
    secret = 'SEC91ab90f92ec8a031f1947092b44a7593f0a897e6e51a32cd899435536f2f231c'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return (timestamp,sign)

def sendText(content,receivers=[]):
    addTagContent = addTag()
    url = 'https://oapi.dingtalk.com/robot/send?access_token=1904b7e7697372f772244981e48ae89e651d19c69da617fb7c3d5a369eec2e0f&timestamp={0}&sign={1}'.format(addTagContent[0],addTagContent[1]) #这里填写你自定义机器人的webhook地址
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    isAtAll = 0 if len(receivers)>0 else 1
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {
            "atMobiles": receivers,
            "isAtAll": isAtAll                                         #如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    # print(res.text)

if __name__ == '__main__':
    sendText("康乐，小葫芦，你们好！",["+86-17667937371","+86-15669937729"])
    sendText("康乐，小葫芦，你们好！")
