# -*- coding:utf-8 -*-
# import re
#
# str1 = '添加大纲3364成功 99'
# pattern = re.compile(r'[^\d]+(\d+)[^\d]+')
# res = re.findall(pattern, str1)
# print res

st = u'南京市'
st1 = u'北京市本级'
a = st.replace(u'本级', u'')
b = st1.replace(u'本级', u'')
print a
print b
