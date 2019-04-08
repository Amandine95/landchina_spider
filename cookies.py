# -*- coding: utf-8 -*-

import sys
import config
import requests
from requests import utils

reload(sys)
sys.setdefaultencoding('utf-8')

url1 = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default'
url2 = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default&security_verify_data=313932302c31303830'


def get_cookies():
    """获取cookies"""
    resp1 = requests.get(url1, headers=config.headers)
    ck1 = resp1.cookies
    cookie_dict = utils.dict_from_cookiejar(ck1)
    config.cookies1.update(cookie_dict)
    resp2 = requests.get(url2, headers=config.headers, cookies=config.cookies1)
    ck2 = resp2.cookies
    cookie_dict = utils.dict_from_cookiejar(ck2)
    config.cookies1.update(cookie_dict)
    return config.cookies1


if __name__ == '__main__':
    get_cookies()
