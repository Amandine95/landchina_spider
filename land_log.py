# -*- coding:utf-8 -*-

import sys
import logging

reload(sys)
sys.setdefaultencoding('utf-8')


def set_log():
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    handler1 = logging.FileHandler(u'log/page.log', 'w+')
    handler1.setLevel(logging.WARNING)
    handler1.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(handler1)

    return logger


if __name__ == '__main__':
    set_log()
