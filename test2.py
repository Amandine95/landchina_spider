# -*- coding:utf-8 -*-

import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read(u'config.ini')
bk = cf.get('key', 'baidu_key')
print type(bk)
