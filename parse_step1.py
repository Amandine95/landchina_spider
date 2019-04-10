# -*- coding: utf-8 -*-

import sys
import requests
import config
from lxml import etree
import datetime
import re
from land_log import set_log
from parse_step2 import parse_detail
from cookies import get_cookies
from land_utils.land_utils.esclient import get_es_client

reload(sys)
sys.setdefaultencoding('utf-8')

logger = set_log()
es = get_es_client()


def set_day(sd, ed):
    """设置日期"""
    while True:
        sd += datetime.timedelta(days=1)
        scratch_date = sd.strftime('%Y-%m-%d')
        yield scratch_date
        if sd == ed:
            break


def get_data(url, date):
    """获取form_data参数"""
    resp = requests.get(url, headers=config.headers, cookies=get_cookies())
    html_div = etree.HTML(resp.content)
    tab = '9f2c3acd-0256-4da2-a659-6949c4671a2a:' + date + '~' + date
    event = html_div.xpath("//*[@id='__EVENTVALIDATION']/@value")[0]
    view = html_div.xpath("//*[@id='__VIEWSTATE']/@value")[0]
    config.formdata['__VIEWSTATE'] = view
    config.formdata['__EVENTVALIDATION'] = event
    config.formdata['TAB_QuerySubmitConditionData'] = tab
    return config.formdata


def parse_day(url, data):
    """按天获取页数"""
    resp = requests.post(url, data=data, headers=config.headers, cookies=get_cookies())
    html_div1 = etree.HTML(resp.text)
    pg_str = html_div1.xpath('//div[@class="pager"]/table/tbody/tr/td[1]/text()')[0]
    print pg_str
    if pg_str:
        pattern = re.compile(ur'[^\d]+(\d+)[^\d]+')
        page = re.findall(pattern, pg_str)
        if page:
            pn = int(page[0])
            return pn


def parse_page(url, page, data):
    """解析每一页"""
    urls = []
    data['TAB_QuerySubmitPagerData'] = '%d' % page
    resp = requests.post(url, data=data, headers=config.headers, cookies=get_cookies())
    html_div2 = etree.HTML(resp.text)
    data_list = html_div2.xpath('//table[@id="TAB_contentTable"]/tbody/tr')
    end = len(data_list) + 1
    for i in range(2, end):
        ul = html_div2.xpath('//table[@id="TAB_contentTable"]/tbody/tr[%d]/td[3]/a/@href' % i)[0]
        urls.append(ul)
    logger.warning(u'page-第%d页' % page)
    print u'第%d页' % page
    yield urls  # 返回每一页url列表


if __name__ == '__main__':
    pre_url = 'http://www.landchina.com/'  # url前缀
    link = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default'  # 初始url
    bk = 'jTkxA1kZ0tGqTpPGYv0DVT701vOQRowI'  # 百度地图key
    tk = 'fd0b585cad4c92e1440c10a0c6bd3c76'  # 天地图key
    sd = datetime.datetime(2018, 11, 22)
    ed = datetime.datetime(2018, 11, 23)
    try:
        for day in set_day(sd, ed):
            logger.warning(u'date-日期%s' % day)
            para = get_data(link, day)
            pg = parse_day(link, para)
            for page in range(4, pg + 1):  # 起始页截止页
                pages_urls = parse_page(link, page, para)  # 所有页的urls列表
                for page_urls in pages_urls:  # u 每一页的urls
                    urls = page_urls
                    for url in urls:
                        index = urls.index(url)
                        logger.warning(u'start-第%d条' % index)
                        dic, content = parse_detail(pre_url, url, bk, tk)
                        es.index("land_transaction_1_cn", "transaction", dic, dic['id'])
                        # print dic['usage_period']
                        logger.warning(u'end-第%d条url;%s' % (index, dic['data_source_url']))
    except Exception as e:
        print e
