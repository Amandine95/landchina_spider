# -*- coding:utf-8 -*-

import re


def test(a):
    a = a if u'人民政府' in a else a + u'人民政府'
    print a


if __name__ == '__main__':
    b = u'市人民政府'
    c = u'区'
    test(b)
    test(c)
