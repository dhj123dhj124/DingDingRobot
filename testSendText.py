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

headers = {"Content-Type": "application/json ;charset=utf-8 "}

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
    res = requests.post(getUrl(robot), data=stringTextMsg, headers=headers)

def sendLink(robot,picUrl = "",messageUrl = "",receivers=[]):
    isAtAll = 0 if len(receivers)>0 else 1
    stringTextMsg = {
    "msgtype": "link", 
    "link": {
        "text": "这个即将发布的新版本，创始人xx称它为红树林。而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是红树林", 
        "title": "时代的火车向前开", 
        "picUrl": picUrl, 
        "messageUrl": messageUrl
        },
    "at": {
        "atMobiles": receivers,
        "isAtAll": isAtAll                                         #如果需要@所有人，这些写1
        }
    }
    stringTextMsg = json.dumps(stringTextMsg)
    res = requests.post(getUrl(robot), data=stringTextMsg, headers=headers)

if __name__ == '__main__':
    # sendText(robots["XDD"],"康乐，你是皮痒了！",["+86-17667937371"])
    # sendText(robots["XDD"],"葫芦憨憨，你那鳖行了！",["+86-15669937729"])
    sendLink(robots["XDD"],"","https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI")