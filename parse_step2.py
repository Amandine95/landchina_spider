# -*- coding: utf-8 -*-

import sys
import requests
import config
from lxml import etree
from utlis import get_date_obj, get_txt
from cookies import get_cookies
from land_utils.land_utils import cityid as ci, geoinformation as geo
import time
import json

# from land_log import set_log

reload(sys)
sys.setdefaultencoding('utf-8')


# logger = set_log()


def parse_detail(url_prefix, urls, bk, tk):
    """遍历列表解析详情页"""
    for url in urls:
        dic = {}
        dic['dis'] = None
        dic['ele_no'] = None
        dic['city'] = None
        dic['province'] = None
        dic['location'] = None
        dic['district'] = None
        dic['land_name'] = None
        dic['land_source'] = u'新增建设用地(库存)'
        dic['usage_level'] = None
        dic['transaction_type_raw'] = None
        dic['usage_period_raw'] = None
        dic['level'] = None
        dic['deal_price'] = None
        dic['area'] = None
        dic['approve_authority'] = None
        dic['transaction_date'] = None
        dic['usage_type'] = None
        dic['plot_ratio_high_raw'] = None
        dic['plot_ratio_low_raw'] = None
        dic['plot_ratio'] = None
        dic['geopoint'], dic['geopoint1'] = {}, {}
        url = url_prefix + url
        resp = requests.get(url, headers=config.headers, cookies=get_cookies())
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
            dic['ele_no'] = ele_no[0]
            pre = dic['ele_no'][0:4]
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
        dic['geopoint']['lat'], dic['geopoint']['lon'] = lat, lon
        dic['geopoint1']['tdt_lat'], dic['geopoint1']['tdt_lon'] = geo.get_tianditu_points(tk, address)
        # 区
        dic['district'] = geo.get_baidu_address(bk, lat, lon)[1]
        # 项目名称
        land_name = table.xpath('./tr[4]/td[2]/span/text()')
        if land_name:
            dic['land_name'] = land_name[0]
        # 土地来源
        s1 = table.xpath('./tr[6]/td[2]/span/text()')
        s2 = table.xpath('./tr[6]/td[4]/span/text()')
        ls1 = float(get_txt(s1))
        ls2 = float(get_txt(s2))
        if ls1 and ls2 and ls1 == ls2:
            dic['land_source'] = u'现有建设用地'
        elif ls2 and ls2 == 0:
            dic['land_source'] = u'新增建设用地'
        # 土地用途
        usage = table.xpath('./tr[7]/td[2]/span/text()')
        if usage:
            key = [k for k, v in config.usage_form.items() if usage[0] in v]
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
        # 土地级别
        level = table.xpath('./tr[9]/td[2]/span/text()')
        if level:
            dic['level'] = level[0]
        # 成交价格
        price = table.xpath('./tr[9]/td[4]/span/text()')
        if price:
            dic['deal_price'] = round(float(price[0]) * 10000, 2)
        # 面积
        area = table.xpath('./tr[6]/td[2]/span/text()')
        if area:
            dic['area'] = round(float(area[0]) * 10000, 2)
        # 批准单位
        approve_authority = table.xpath('./tr[16]/td[2]/span/text()')
        if approve_authority:
            dic['approve_authority'] = approve_authority[0]
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
        dic['plot_ratio_low_raw'] = get_txt(min_limit)
        dic['plot_ratio_high_raw'] = get_txt(max_limit)
        if min_limit:
            dic['plot_ratio'] = float(dic['plot_ratio_low_raw'])
        elif max_limit:
            dic['plot_ratio'] = float(dic['plot_ratio_high_raw'])
        # 数据源
        dic['data_source_url'] = url
        # id
        dic['id'] = url[121:]
        # 处理时间
        dic['deal_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return dic, content


if __name__ == '__main__':
    url_pre = 'http://www.landchina.com/'
    url_list = [
        'default.aspx?tabid=386&comname=default&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&recorderguid=c3306301-f607-4808-95c1-27de1faba4dd']
    bk = 'jTkxA1kZ0tGqTpPGYv0DVT701vOQRowI'
    tk = 'fd0b585cad4c92e1440c10a0c6bd3c76'
    parse_detail(url_pre, url_list, bk, tk)
