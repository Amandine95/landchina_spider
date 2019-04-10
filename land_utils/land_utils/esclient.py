# -*- coding:utf-8 -*-

import sys
import os
from elasticsearch import Elasticsearch

reload(sys)
sys.setdefaultencoding('utf-8')

settings = {"elsticsearch_nodes": ['192.168.1.135:29200']}
es_dict = {}


def get_es_client():
    pid = os.getpid()
    if pid in es_dict:
        return es_dict[pid]
    else:
        es_client = Elasticsearch(
            settings['elsticsearch_nodes'],
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60,
            maxsize=10
        )
        es_dict[pid] = es_client
        return es_client


def is_new(url, index_name, index_type):
    """判断详情url是否存在es"""
    sql = '{"query":{"bool":{"must":[{"term":{"data_source_url":"%s"}}],"must_not":[],"should":[]}},"from":0,"size":250,"sort":[],"aggs":{}}' % url
    es = get_es_client()
    try:
        result = es.search(index_name, index_type, body=sql)['hits']['total']
        return result
    except Exception as e:
        print e
