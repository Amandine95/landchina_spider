# -*- coding:utf-8 -*-
from urllib import quote, urlopen
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_baidu_points(bk, address):
    """
    获取百度坐标
    :param bk: 开发者key
    :param address: 地址
    :return: lat,lon
    """
    tries = 5
    while tries > 0:
        try:
            address = address.replace(u'、', u'') if u'、' in address else address
            address = address.encode('utf-8') if type(address) != 'str' else address
            url = 'http://api.map.baidu.com/geocoder/v2/'
            output = 'json'
            add = quote(address)  # 信息格式化
            uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + bk
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


def get_baidu_address(bk, lat, lon):
    """
    根据坐标获取地址
    :param bk: key
    :param lat: 经度
    :param lon: 纬度
    :return: 地址
    """
    tries = 5
    while tries > 0:
        try:
            url = 'http://api.map.baidu.com/geocoder/v2/'
            output = 'json'
            location = str(lat) + ',' + str(lon)
            lastest_admin = "1"  # 是否访问最新版行政区划分数据 1是0否
            uri = url + '?location=' + location + "&output=" + output + "&pois=1&ak=" + bk + "&lastest_admin" + lastest_admin

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


def get_tianditu_points(tk, address):
    """
    获取天地图坐标
    :param tk: 开发者key
    :param address: 地址
    :return: lat,lon
    """
    tries = 5
    while tries > 0:
        try:
            ds_dict = {}
            address = address.encode('utf-8') if type(address) != 'str' else address
            url = 'http://api.tianditu.gov.cn/geocoder'
            address = quote(address)
            ds_dict["keyWord"] = address
            data = json.dumps(ds_dict)
            uri = url + '?' + 'ds=' + data + '&tk=' + tk
            resp = urlopen(uri)
            resp_data = json.loads(resp.read())
            if resp_data['status'] == '0':
                lat = resp_data['location']['lat']
                lon = resp_data['location']['lon']
                return float(lat), float(lon)
            else:
                tries -= 1
                continue
        except Exception as e:
            print 'tianditu-1', e
            tries -= 1
            continue
    lat = float(0)
    lon = float(0)
    return lat, lon


if __name__ == '__main__':
    bk = 'jTkxA1kZ0tGqTpPGYv0DVT701vOQRowI'
    address = u'阜阳市颍泉区伍明沟东侧、规划茨河路北侧'
    print get_baidu_points(bk,address)

