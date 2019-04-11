# -*- coding: utf-8 -*-

import sys
import params
import requests
from requests import utils

reload(sys)
sys.setdefaultencoding('utf-8')

url1 = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default'
url2 = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default&security_verify_data=313932302c31303830'


def get_cookies():
    """获取cookies"""
    resp1 = requests.get(url1, headers=params.headers)
    ck1 = resp1.cookies
    cookie_dict = utils.dict_from_cookiejar(ck1)
    params.cookies1.update(cookie_dict)
    resp2 = requests.get(url2, headers=params.headers, cookies=params.cookies1)
    ck2 = resp2.cookies
    cookie_dict = utils.dict_from_cookiejar(ck2)
    params.cookies1.update(cookie_dict)
    return params.cookies1


if __name__ == '__main__':
    get_cookies()
