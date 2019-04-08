# -*- coding:utf-8 -*-

import sys
from esclient import get_es_client

reload(sys)
sys.setdefaultencoding('utf-8')
es = get_es_client()


def get_city_province(data, index_name="region_metadata_2017_cn"):
    """
    获取省市
    :param data: city_id前缀4位或行政区
    :param index_name: 省市es索引
    :return: city、province
    """
    if u'本级' in data:
        sql = '{"query":{"bool":{"must":[{"term":{"city":"%s"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}' % data.replace(
            u'本级', u'')
    elif data.isdigit():
        sql = '{"query":{"bool":{"must":[{"prefix":{"city_id":"%s"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}' % data
    else:
        sql = '{"query":{"bool":{"must":[{"term":{"county":"%s"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}' % data
    try:
        res = es.search(index_name, "meta", body=sql)['hits']['hits']
        if len(res):
            city_name = res[0]['_source']['city']
            province_name = res[0]['_source']['province']
        else:
            city_name = ''
            province_name = ''
        return city_name, province_name
    except Exception as e:
        print e


if __name__ == '__main__':
    print get_city_province('3209')[1]
