# -*- coding:utf-8 -*-

import requests
import params

headers = params.headers
url = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default'

# proxies = {
#     'http': '223.223.203.78:8080'
# }

resp = requests.get(url=url, headers=headers)

print resp.text
