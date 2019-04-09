# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

cookies1 = {

    'srcurl': '687474703a2f2f7777772e6c616e646368696e612e636f6d2f64656661756c742e617370783f74616269643d32363326436f6d4e616d653d64656661756c74',
    'ASP.NET_SessionId': 'imrh1utgzcj5piuwdtnaomuh',
    'Hm_lvt_83853859c7247c5b03b527894622d3fa': '1554342276',
    'Hm_lpvt_83853859c7247c5b03b527894622d3fa': '1554342276'
}

formdata = {
    '__VIEWSTATE': None,
    '__EVENTVALIDATION': None,
    'hidComName': 'default',
    'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
    'TAB_QuerySortItemList': '282:False',
    'TAB_QuerySubmitOrderData': '282:False',
    'TAB_RowButtonActionControl': '',
    'TAB_QuerySubmitPagerData': '1',
    'TAB_QuerySubmitSortData': ''
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    'Connection': 'close'
}

params = {
    'tabid': '261',
    'ComName': 'default'
}

province_code = {"11": u"北京市", "12": u"天津市", "13": u"河北省", "14": u"山西省", "15": u"内蒙古", "21": u"辽宁省", "22": u"吉林省",
                 "23": u"黑龙江省", "31": u"上海市", "32": u"江苏省", "33": u"浙江省", "34": u"安徽省", "35": u"福建省", "36": u"江西省",
                 "37": u"山东省", "41": u"河南省", "42": u"湖北省", "43": u"湖南省", "44": u"广东省", "45": u"广西壮族", "46": u"海南省",
                 "50": u"重庆市", "51": u"四川省", "52": u"贵州省", "53": u"云南省", "54": u"西藏", "61": u"陕西省", "62": u"甘肃省",
                 "63": u"青海省", "64": u"宁夏回族", "65": u"新疆维吾尔", "66": u"新疆建设兵团", "71": u"台湾省", "81": u"香港特别行政区",
                 "82": u"澳门特别行政区"}

usage_form = {
    u'住宅': u'高档住宅用地_中低价位、中小套型普通商品住房用地_其他普通商品住房用地_经济适用住房用地_其他住房用地_廉租住房用地_住宅用地_公共租赁住房用地_限价商品房_城镇住宅用地',
    u'商服': u'批发零售用地_住宿餐饮用地_商务金融用地_其他商服用地_商服用地',
    u'工业': u'工业用地_采矿用地_仓储用地_工矿仓储用地',
    u'公共事业': u'机关团体用地_新闻出版用地_科教用地_医卫慈善用地_文体娱乐用地_公共设施用地_公园与绿地_风景名胜设施用地_公共管理与公共服务用地',
    u'特殊': u'军事设施用地_使领馆用地_监教场所用地_宗教用地_殡葬用地_特殊用地',
    u'交通运输': u'铁路用地_公路用地_街巷用地_机场用地_港口码头用地_管道运输用地_农村道路_交通运输用地',
    u'水域及水利设施': u'河流水面_湖泊水面_水库水面_坑塘水面_沿海滩涂_内陆滩涂_沟渠_水工建筑用地_冰川及永久积雪_水域及水利设施用地',
    u'其他': u'空闲地_设施农用地_田坎_盐碱地_沼泽地_沙地_裸地_其他土地'
}
