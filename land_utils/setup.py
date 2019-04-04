# -*- coding: utf-8 -*-

import sys
from setuptools import setup

reload(sys)
sys.setdefaultencoding('utf-8')

setup(name='land_utils',
      version='0.1',
      description='some utils for land china spiders',
      author='LiYiXin',
      packages=['land_utils', 'filter'],
      zip_safe=False)
