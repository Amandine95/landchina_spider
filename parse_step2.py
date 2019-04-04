# -*- coding: utf-8 -*-

import sys
import requests
import config
from lxml import etree

# from land_log import set_log

reload(sys)
sys.setdefaultencoding('utf-8')


# logger = set_log()


def parse_detail(url_prefix, urls):
    """遍历列表解析详情页"""
    for url in urls:
        dic = {}
        url = url_prefix + url
        resp = requests.get(url, headers=config.headers, cookies=config.cookies3)
        # print resp.text
        html_div = etree.HTML(resp.text)
        table = html_div.xpath('//*[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1"]/tbody')[0]
        dic['city'] = table.xpath('./tr[3]/td[2]/span/text()')[0]
        dic['ele_no'] = table.xpath('./tr[3]/td[4]/span/text()')[0]
        dic['location'] = table.xpath('./tr[5]/td[2]/span/text()')[0]
        dic['land_name'] = table.xpath('./tr[4]/td[2]/span/text()')[0]
        dic['land_source'] = table.xpath('./tr[6]/td[4]/span/text()')[0]
        dic['land_usage'] = table.xpath('./tr[7]/td[2]/span/text()')[0]
        dic['transaction_type_raw'] = table.xpath('./tr[7]/td[4]/span/text()')[0]
        dic['usage_period_raw'] = table.xpath('./tr[8]/td[2]/span/text()')[0]
        area = table.xpath('./tr[6]/td[2]/span/text()')[0]
        print type(area)
        dic['area'] = round(float(area) * 10000, 2)
        print dic


if __name__ == '__main__':
    url_pre = 'http://www.landchina.com/'
    url_list = [
        'default.aspx?tabid=386&comname=default&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&recorderguid=c3306301-f607-4808-95c1-27de1faba4dd']
    parse_detail(url_pre, url_list)
