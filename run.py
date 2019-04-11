# -*- coding: utf-8 -*-

import sys
import requests
import params
from lxml import etree
import datetime
import re
from land_log import set_log
from parse_detail import parse_detail
from cookies import get_cookies
from land_utils.land_utils.esclient import get_es_client, is_new
from requests.adapters import HTTPAdapter
import time
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

logger = set_log()
es = get_es_client()

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=5))  # 增加重试次数
s.keep_alive = False  # 关闭多余连接


def set_day(sd, ed):
    """设置日期"""
    while True:
        sd += datetime.timedelta(days=1)
        scratch_date = sd.strftime('%Y-%m-%d')
        yield scratch_date
        if sd == ed:
            break


def get_data(url, date, cookies):
    """获取form_data参数"""
    resp = requests.get(url, headers=params.headers, cookies=cookies)
    html_div = etree.HTML(resp.content)
    tab = '9f2c3acd-0256-4da2-a659-6949c4671a2a:' + date + '~' + date
    event = html_div.xpath("//*[@id='__EVENTVALIDATION']/@value")[0]
    view = html_div.xpath("//*[@id='__VIEWSTATE']/@value")[0]
    params.formdata['__VIEWSTATE'] = view
    params.formdata['__EVENTVALIDATION'] = event
    params.formdata['TAB_QuerySubmitConditionData'] = tab
    return params.formdata


def parse_day(url, data, cookies):
    """按天获取页数"""
    resp = requests.post(url, data=data, headers=params.headers, cookies=cookies)
    html_div1 = etree.HTML(resp.text)
    pg_str = html_div1.xpath('//div[@class="pager"]/table/tbody/tr/td[1]/text()')[0]
    if pg_str:
        pattern = re.compile(ur'[^\d]+(\d+)[^\d]+')
        page = re.findall(pattern, pg_str)
        if page:
            pn = int(page[0])
            print u'共%d页' % pn
            return pn


def parse_page(url, page, data, cookies):
    """解析每一页"""
    urls = []
    data['TAB_QuerySubmitPagerData'] = '%d' % page
    resp = requests.post(url, data=data, headers=params.headers, cookies=cookies)
    html_div2 = etree.HTML(resp.text)
    data_list = html_div2.xpath('//table[@id="TAB_contentTable"]/tbody/tr')
    end = len(data_list) + 1
    for i in range(2, end):
        ul = html_div2.xpath('//table[@id="TAB_contentTable"]/tbody/tr[%d]/td[3]/a/@href' % i)[0]
        urls.append(ul)
    logger.warning(u'page-第%d页' % page)
    print u'第%d页' % page
    yield urls  # 返回每一页url列表


cf = ConfigParser.ConfigParser()  # 读取配置文件
cf.read(u'config.ini')
cookie = get_cookies()  # 获取cookies
pre_url = 'http://www.landchina.com/'  # url前缀
link = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default'  # 初始url
bk = cf.get('key', 'baidu_key')  # 百度地图key
tk = cf.get('key', 'tianditu_key')  # 天地图key
index_name = cf.get('es_index', 'index_name')
index_type = cf.get('es_index', 'index_type')
sd = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
ed = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
for day in set_day(sd, ed):
    print u'日期:%s' % day
    logger.warning(u'date-日期%s' % day)
    para = get_data(link, day, cookie)
    pg = parse_day(link, para, cookie)
    for page in range(1, pg + 1):  # 起始页截止页
        pages_urls = parse_page(link, page, para, cookie)  # 所有页的urls列表
        for page_urls in pages_urls:  # u 每一页的urls
            urls = page_urls
            for url in urls:
                time.sleep(3)
                u = pre_url + url
                res = is_new(u, index_name, index_type)  # 判断是否已存入es
                # 不存在es里
                if not res:
                    index = urls.index(url)
                    try:
                        logger.warning(u'start-第%d条' % index)
                        dic, content = parse_detail(pre_url, url, bk, tk, cookie)
                        es.index(index_name, index_type, dic, dic['id'])
                        logger.warning(u'end-第%d条url;%s' % (index, dic['data_source_url']))  # 成功的url
                    except Exception as e:
                        print e
                        logger.warning(u'fail_url-%s' % u)  # 失败的url
                        continue

                else:
                    continue
