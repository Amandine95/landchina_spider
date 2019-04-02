# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class LandchinaSpider(scrapy.Spider):
    name = 'landchina'
    allowed_domains = ['www.landchina.com']
    start_urls = ['http://www.landchina.com/default.aspx?tabid=263&ComName=default']
    cookies = {
        'yunsuo_session_verify': '81af70ce64a864693ffc7b62a526e6ea',
        'srcurl': '687474703a2f2f7777772e6c616e646368696e612e636f6d2f64656661756c742e617370783f74616269643d32363326436f6d4e616d653d64656661756c74',
        'security_session_mid_verify': '3701410f83feb9248355c973f9c55ab7',
        'ASP.NET_SessionId': '4c4kav4gxmggejultwjgn0mx',
        'Hm_lvt_83853859c7247c5b03b527894622d3fa': '1552958292',
        'Hm_lpvt_83853859c7247c5b03b527894622d3fa': '1552961183'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, cookies=self.cookies)

    def parse(self, response):
        pg = response.xpath('//div[@class="pager"]/table/tbody/tr/td[1]/text()').extract()
        print pg
        EVENTVALIDATION = response.xpath("//*[@id='__EVENTVALIDATION']/@value").extract()
        VIEWSTATE = response.xpath("//*[@id='__VIEWSTATE']/@value").extract()
        formdatas = {
            '__VIEWSTATE': VIEWSTATE,
            '__EVENTVALIDATION': EVENTVALIDATION,
            'hidComName': 'default',
            'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
            'TAB_QuerySortItemList': '282:False',
            'TAB_QuerySubmitOrderData': '282:False',
            'TAB_RowButtonActionControl': '',
            'TAB_QuerySubmitPagerData': '1',
            'TAB_QuerySubmitSortData': ''
        }
        self.cookies = {
            'yunsuo_session_verify': '81af70ce64a864693ffc7b62a526e6ea',
            'security_session_mid_verify': '3701410f83feb9248355c973f9c55ab7',
            'Hm_lvt_83853859c7247c5b03b527894622d3fa': '1552967955,1553156770,1553667111,1553847211',
            'ASP.NET_SessionId': 'viakdh5umtoizzrvt2dt22ai',
            'Hm_lpvt_83853859c7247c5b03b527894622d3fa': '1553847216'
        }
        # 日期范围
        sd = datetime.datetime(2019, 3, 27)
        ed = datetime.datetime(2019, 3, 28)
        while True:
            sd += datetime.timedelta(days=1)
            scratch_date = sd.strftime('%Y-%m-%d')
            formdatas[
                'TAB_QuerySubmitConditionData'] = '9f2c3acd-0256-4da2-a659-6949c4671a2a:' + scratch_date + '~' + scratch_date
            link = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default'
            yield scrapy.FormRequest(link, callback=self.page_total_count, formdata=formdatas,
                                     cookies=self.cookies,
                                     meta={"day": scratch_date})
            if sd == ed:
                break

    def page_total_count(self, response):
        pn = 1
        print response.text
        page_bar = response.xpath('//div[@class="pager"]/table/tbody/tr/td[1]/text()').extract()
        print page_bar
        # pbs = get_str(page_bar)
        if page_bar:
            page = re.compile(ur'共(\d+)页').findall(page_bar[0])
            if page:
                pn = int(page[0])
        # sp2_url = response.meta['day'] + self.confs['separator'] + str(pn)
        # print u'共  %d 页' % pn
        print pn
        # print u'存入 %s' % sp2_url
