#!/usr/bin/env python3
# encoding: utf-8

import json
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse

robots={"XDD":{"webhook":"https://oapi.dingtalk.com/robot/send?access_token=1904b7e7697372f772244981e48ae89e651d19c69da617fb7c3d5a369eec2e0f","secret":"SEC91ab90f92ec8a031f1947092b44a7593f0a897e6e51a32cd899435536f2f231c"},
        }

#通过机器人的额签名，组织出用于调用的Url
def getUrl(robot):
    timestamp = str(round(time.time() * 1000))
    secret = robot["secret"] 
    secretEnc = secret.encode('utf-8')
    stringToSign = '{}\n{}'.format(timestamp, secret)
    stringToSignEnc = stringToSign.encode('utf-8')
    hmacCode = hmac.new(secretEnc, stringToSignEnc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmacCode))
    return robot["webhook"] + "&timestamp={0}&sign={1}".format(timestamp,sign)

#通过特定机器人向特定用户发送消息
def sendText(robot,content = "",receivers=[]):
    url = getUrl(robot)
    headers = {"Content-Type": "application/json ;charset=utf-8 "}
    isAtAll = 0 if len(receivers)>0 else 1
    stringTextMsg = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {
            "atMobiles": receivers,
            "isAtAll": isAtAll                                         #如果需要@所有人，这些写1
        }
    }
    stringTextMsg = json.dumps(stringTextMsg)
    res = requests.post(url, data=stringTextMsg, headers=headers)

if __name__ == '__main__':
    sendText(robots["XDD"],"`",["+86-17667937371"])
