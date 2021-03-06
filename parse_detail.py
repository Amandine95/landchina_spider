# -*- coding: utf-8 -*-

import sys
import requests
import params
from lxml import etree
from utils import get_date_obj, get_txt
from land_utils.land_utils import cityid as ci, geoinformation as geo
import time
import re

reload(sys)
sys.setdefaultencoding('utf-8')


def parse_detail(url_prefix, url, bk, tk, cookies):
    """解析详情页"""
    dic = {}
    dic['dis'] = None
    dic['electr_supervise_no'] = None
    dic['city'] = None
    dic['province'] = None
    dic['location'] = None
    dic['district'] = None
    dic['land_name'] = None
    dic['land_source'] = u'新增建设用地(库存)'
    dic['usage_level'] = None
    dic['usage_level2'] = None
    dic['transaction_type_raw'] = None
    dic['usage_period_raw'] = None
    dic['usage_period'] = None
    dic['level'] = None
    dic['deal_price_raw'] = None
    dic['deal_price'] = None
    dic['area_total_raw'] = None
    dic['area_total'] = None
    dic['land_transaction_price'] = None
    dic['approve_authority'] = None
    dic['transaction_date'] = None
    dic['usage_type'] = None
    dic['plot_ratio_high_raw'] = None
    dic['plot_ratio_low_raw'] = None
    dic['plot_ratio'] = None
    dic['receive_institution'] = None
    dic['geopoint'], dic['geopoint1'] = {}, {}
    url = url_prefix + url
    resp = requests.get(url, headers=params.headers, cookies=cookies, timeout=10)
    print u'------------拿到页面--------------------'
    html_div = etree.HTML(resp.text)
    table = html_div.xpath('//*[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1"]/tbody')[0]  # 数据所在table
    content = etree.tostring(table, method='html')
    # 行政区
    dis = table.xpath('./tr[3]/td[2]/span/text()')
    if dis:
        dic['dis'] = dis[0]
    # 电子监管号
    ele_no = table.xpath('./tr[3]/td[4]/span/text()')
    # 存在电子监管号
    if ele_no:
        dic['electr_supervise_no'] = ele_no[0]
        pre = dic['electr_supervise_no'][0:4]
        # 市、省
        dic['city'], dic['province'] = ci.get_city_province(pre)
    # 不存在监管号
    else:
        data = dic['dis']
        dic['city'], dic['province'] = ci.get_city_province(data)
    # 地理位置
    location = table.xpath('./tr[5]/td[2]/span/text()')
    if location:
        dic['location'] = location[0]
    address = dic['city'] + dic['location']
    # 坐标
    lat, lon = geo.get_baidu_points(bk, address)
    print u'-------------百度坐标-------------------'
    dic['geopoint']['lat'], dic['geopoint']['lon'] = lat, lon
    dic['geopoint1']['tdt_lat'], dic['geopoint1']['tdt_lon'] = geo.get_tianditu_points(tk, address)
    print u'-------------天地图坐标-----------------'
    # 区
    if u'本级' not in dic['dis']:
        dic['district'] = dic['dis']
    else:
        dic['district'] = geo.get_baidu_address(bk, lat, lon)[1]
    # 项目名称
    land_name = table.xpath('./tr[4]/td[2]/span/text()')
    if land_name:
        dic['land_name'] = land_name[0]
    # 土地来源
    s1 = table.xpath('./tr[6]/td[2]/span/text()')
    s2 = table.xpath('./tr[6]/td[4]/span/text()')
    ls1, ls2 = None, None
    if s1:
        ls1 = float(get_txt(s1))
    if s2:
        ls2 = float(get_txt(s2))
    if ls1 and ls2 and ls1 == ls2:
        dic['land_source'] = u'现有建设用地'
    elif ls2 and ls2 == 0:
        dic['land_source'] = u'新增建设用地'
    # 土地用途
    usage = table.xpath('./tr[7]/td[2]/span/text()')
    if usage:
        dic['usage_level2'] = usage[0]
        key = [k for k, v in params.usage_form.items() if usage[0] in v]
        if key:
            dic['usage_level'] = key[0]
    # 供地方式
    transaction_type_raw = table.xpath('./tr[7]/td[4]/span/text()')
    if transaction_type_raw:
        dic['transaction_type_raw'] = transaction_type_raw[0]
    # 土地使用年限
    usage_period_raw = table.xpath('./tr[8]/td[2]/span/text()')
    if usage_period_raw:
        dic['usage_period_raw'] = usage_period_raw[0]
        if dic['usage_period_raw'].isdigit():
            dic['usage_period'] = float(dic['usage_period_raw'])
        else:
            res = dic['usage_period_raw'].split(u';')
            for i in res:
                if dic['usage_level2'] in i:
                    dic['usage_period'] = float(re.match(ur'.*?(\d+)', i).group(1))
    # 土地级别
    level = table.xpath('./tr[9]/td[2]/span/text()')
    if level:
        dic['level'] = level[0]
    # 成交价格
    price = table.xpath('./tr[9]/td[4]/span/text()')
    if price:
        dic['deal_price_raw'] = price[0]
        dic['deal_price'] = round(float(price[0]) * 10000, 2)
    # 面积
    area = table.xpath('./tr[6]/td[2]/span/text()')
    if area:
        dic['area_total_raw'] = area[0]
        dic['area_total'] = round(float(area[0]) * 10000, 2)
    # 单价
    if dic['deal_price'] and dic['area_total']:
        dic['land_transaction_price'] = float(dic['deal_price'] / dic['area_total'])
    # 批准单位
    approve_authority = table.xpath('./tr[16]/td[2]/span/text()')
    if approve_authority:
        dic['approve_authority'] = approve_authority[0] if u'人民政府' in approve_authority[0] else approve_authority[
                                                                                                    0] + u'人民政府'
    # 成交日期
    date = table.xpath('./tr[16]/td[4]/span/text()')
    if date:
        dic['transaction_date'] = get_date_obj(date[0])
    # 行业分类
    usage_type = table.xpath('./tr[8]/td[4]/span/text()')
    if usage_type:
        dic['usage_type'] = usage_type[0]
    # 容积率
    min_limit = table.xpath('tr[13]/td[2]//tr[2]/td[2]/span/text()')
    max_limit = table.xpath('tr[13]/td[2]//tr[2]/td[4]/span/text()')
    if min_limit:
        dic['plot_ratio_low_raw'] = get_txt(min_limit)
        dic['plot_ratio'] = float(dic['plot_ratio_low_raw'])
    if max_limit:
        dic['plot_ratio_high_raw'] = get_txt(max_limit)
        dic['plot_ratio'] = float(dic['plot_ratio_high_raw'])
    # 土地使用权人
    per1 = table.xpath('tr[11]/td[2]/span/text()')
    per2 = table.xpath('tr[12]/td[1]/span/text()')
    if per1:
        dic['receive_institution'] = per1[0]
    elif per2:
        dic['receive_institution'] = per2[0]
    # 数据源
    dic['data_source_url'] = url
    # id
    dic['id'] = url[121:]
    # 处理时间
    dic['crawl_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    dic['data_source'] = u'中国土地市场网'
    return dic, content


if __name__ == '__main__':
    url_pre = 'http://www.landchina.com/'
    url = 'default.aspx?tabid=386&comname=default&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&recorderguid=c3306301-f607-4808-95c1-27de1faba4dd'
    bk = 'jTkxA1kZ0tGqTpPGYv0DVT701vOQRowI'
    tk = 'fd0b585cad4c92e1440c10a0c6bd3c76'
    # print parse_detail(url_pre, url, bk, tk,)[0]
