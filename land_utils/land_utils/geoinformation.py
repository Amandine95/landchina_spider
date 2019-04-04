# -*- coding:utf-8 -*-
from urllib import quote, urlopen
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_baidu_points(address):
    tries = 5
    while tries > 0:
        try:
            address = address.replace(u'、', u'') if u'、' in address else address
            address = address.encode('utf-8') if type(address) != 'str' else address
            url = 'http://api.map.baidu.com/geocoder/v2/'
            output = 'json'
            ak = 'jTkxA1kZ0tGqTpPGYv0DVT701vOQRowI'
            add = quote(address)  # 信息格式化
            uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
            req = urlopen(uri)
            res = req.read()
            temp = json.loads(res)
            if temp['status'] == 0:
                lat = temp['result']['location']['lat']
                lng = temp['result']['location']['lng']
                return lat, lng
            else:
                tries -= 1
                continue

        except Exception, e:
            print 'get_coordinate-1', e
            tries -= 1
            continue
    lat = float(0)
    lon = float(0)

    return lat, lon


def get_baidu_address(lat, lon):
    tries = 5
    while tries > 0:
        try:
            url = 'http://api.map.baidu.com/geocoder/v2/'
            output = 'json'
            ak = 'jTkxA1kZ0tGqTpPGYv0DVT701vOQRowI'
            location = str(lat) + ',' + str(lon)
            lastest_admin = "1"  # 是否访问最新版行政区划分数据 1是0否
            uri = url + '?location=' + location + "&output=" + output + "&pois=1&ak=" + ak + "&lastest_admin" + lastest_admin

            req = urlopen(uri)
            res = req.read()
            result = json.loads(res)
            if result['status'] == 0:
                city = result['result']['addressComponent']['city']
                dstrict = result['result']['addressComponent']['district']
                return city, dstrict
            else:
                tries -= 1
                continue

        except Exception, e:
            print 'get_coordinate2-', e
            tries -= 1
            continue

    city = None
    district = None
    return city, district





