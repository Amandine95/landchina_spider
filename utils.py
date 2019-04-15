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


def get_txt(li):
    """列表转字符串"""
    return ''.join(li).replace(u'\xa0', u'')


def get_end_day():
    """获取成功日期"""
    day_list = []
    with open(u'log/page.log', 'r+') as f:
        res = f.readlines()
        for line in res:
            if u'day_end' in line:
                t = line.split('--')[1].replace(u'\n', '')
                day_list.append(t)
        new_list = list(set(day_list))
        new_list.sort(key=day_list.index)
        return new_list


def get_end_page(day):
    """获取完后的页数"""
    page_list = []
    with open(u'log/page.log', 'r+') as f:
        res = f.readlines()
        for line in res:
            if u'page_end--%s' % day in line:
                t = line.split('--')[2].replace(u'\n', u'')
                page_list.append(int(t))
        new_list = list(set(page_list))
        new_list.sort(key=page_list.index)
        return new_list


if __name__ == '__main__':
    st = u'2017年09月11日'
    print get_date_obj(st)
