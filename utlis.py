# -*- coding: utf-8 -*-

import sys
import datetime
import re

reload(sys)
sys.setdefaultencoding('utf-8')


def get_date_obj(string):
    """获取日期对象"""
    if not string:
        return
    substitute_list = [u'年', u'月', u'日']
    for x in substitute_list:
        string = string.replace(x, u'-')
    if string.endswith(u'-'):
        string = string[:-1]
        try:
            y_m_d = re.compile(u"\d{4}-[0-9]{1,2}-[0-9]{1,2}").findall(string)
            if y_m_d:
                date_std = datetime.datetime.strptime(y_m_d[0], u"%Y-%m-%d").strftime(u"%Y-%m-%d")
            else:
                date_std = None
            return date_std
        except Exception, e:
            print e
            return


if __name__ == '__main__':
    st = u'2017年09月11日'
    print get_date_obj(st)
