from datetime import datetime
from urllib.request import urlopen
import time
import json
import sys

sys.path.append("../../")

from server.database.model import WxInfo
from server.wx.configure import appId, appSecret


class Basic:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0
        self.__jsapi_ticket = ''
        self.__leftTime_ticket = 0

    def __real_get_access_token(self):
        # 获取 access_token
        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
                   "client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = urlopen(postUrl)
        urlResp = json.loads(urlResp.read())
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

        # 获取 jsapi_ticket
        postUrl_1 = ("https://api.weixin.qq.com/cgi-bin/ticket/getticket?"
                     "access_token=%s&type=jsapi" % self.__accessToken)
        urlResp_1 = urlopen(postUrl_1)
        urlResp_1 = json.loads(urlResp_1.read())
        self.__jsapi_ticket = urlResp_1['ticket']
        self.__leftTime_ticket = urlResp_1['expires_in']

        accessToken = WxInfo.get(key='accessToken')
        accessToken.value = self.__accessToken
        accessToken.date = datetime.utcnow()
        accessToken.expires_in = self.__leftTime
        accessToken.save()
        jsapi_ticket = WxInfo.get(key='jsapi_ticket')
        jsapi_ticket.value = self.__jsapi_ticket
        jsapi_ticket.date = datetime.utcnow()
        jsapi_ticket.expires_in = self.__leftTime_ticket
        jsapi_ticket.save()

    def get_access_token(self):
        if self.__leftTime < 100:
            self.__real_get_access_token()
        return self.__accessToken

    def run(self):
        while True:
            if self.__leftTime > 100:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()


def wx_access_token_script():
    basic = Basic()
    basic.run()


if __name__ == '__main__':
    wx_access_token_script()
