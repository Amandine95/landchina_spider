# -*- coding:utf-8 -*-
import re
str1 = '添加大纲3364成功 99'
pattern = re.compile(r'[^\d]+(\d+)[^\d]+')
res = re.findall(pattern, str1)
print res
# import requests
# from lxml import etree
#
#
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#                   ' (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
# }
# paras = {
#     'tabid': '261',
#     'ComName': 'default'
# }
#
# url = 'http://www.landchina.com/default.aspx'
#
# cookies = {
#     'yunsuo_session_verify': '81af70ce64a864693ffc7b62a526e6ea',
#     'srcurl': '687474703a2f2f7777772e6c616e646368696e612e636f6d2f64656661756c742e617370783f74616269643d32363326436f6d4e616d653d64656661756c74',
#     'security_session_mid_verify': '3701410f83feb9248355c973f9c55ab7',
#     'ASP.NET_SessionId': '4c4kav4gxmggejultwjgn0mx',
#     'Hm_lvt_83853859c7247c5b03b527894622d3fa': '1552958292',
#     'Hm_lpvt_83853859c7247c5b03b527894622d3fa': '1552961183'
# }
#
# resp = requests.get(url=url, headers=headers, cookies=cookies, params=paras)
# html_div = etree.HTML(resp.content)
# tr_list = html_div.xpath('//*[@id="TAB_contentTable"]//tr[position()>1]')[0]
# pg = html_div.xpath('//div[@class="pager"]/table/tbody/tr/td[1]/text()')[0]
#
# print(tr_list)
# print pg
