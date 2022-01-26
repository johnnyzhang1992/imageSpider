# !/usr/bin/python
# encoding:utf-8
# 这个例子是去获取微博里的图片，例子爬取的微博是欧阳娜娜：2687827715

import time
import requests
import urllib.request
import json
import os
import ssl
ssl._create_default_https_context= ssl._create_unverified_context

from faker import Faker
faker=Faker('zh_CN')
ua=faker.chrome()

request_params = {"ajwvr": "6", "domain": "100505", "domain_op": "100505",
                  "feed_type": "0", "is_all": "1", "is_tag": "0", "is_search": "0"}
profile_request_params = {"profile_ftype": "1", "is_all": "1"}

weibo_url = "https://m.weibo.cn/"
# WEIBO_SECOND_PROFILE_WEIBO 全部
# WEIBO_SECOND_PROFILE_WEIBO_ORI 原创
# WEIBO_SECOND_PROFILE_WEIBO_VIDEO 视频
# WEIBO_SECOND_PROFILE_WEIBO_ARTICAL 文章
# WEIBO_SECOND_PROFILE_WEIBO_WEIBO_SECOND_PROFILE_WEIBO_PIC 文章

# 下面 ID 为欧阳娜娜的微博 ID
# star_id = 2687827715
star_id = input('请输入star_id:')
# 输入上次结束时的 since_id ,可以从上次中断时开始下载
# 从对应目录下 record.text 文件内取值
input_since_id = input("请输入 since_id:")

# 字段拼接
containerid = '107603'+star_id

# https://m.weibo.cn/api/container/getIndex?jumpfrom=weibocom&type=uid&value=2687827715&containerid=1076032687827715&since_id=4720786105434427
baseUrl = 'https://m.weibo.cn/api/container/getIndex?jumpfrom=weibocom&type=uid'
_url =  baseUrl + '&value='+star_id+'&containerid='+containerid

# 最好使用真实的
cookie = 'WEIBOCN_FROM=1110003030; OUTFOX_SEARCH_USER_ID_NCOO=123636308.59677954; SCF=AhTMNl9bAeJagBTL5WGe7GNzjCkO383UWVTXYQT7GOZl_moFcko7o_e4THpdktKfDvh_so5KnHRtQmyCQgv0IyQ.; SUHB=0QS5d_Aa7-wF5m; _T_WM=08780ade7cbb594bc7f80e940f617a83; SSOLoginState=1548123454; ALF=1550715454; MLOGIN=0; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302831246229612%26fid%3D2304131246229612_-_WEIBO_SECOND_PROFILE_WEIBO_PIC%26uicode%3D10000011'

# User-Agent需要根据每个人的电脑来修改
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded',
	'Host':'m.weibo.cn',
	'Pragma':'no-cache',
	'Referer':_url,
	'User-Agent':ua,
	'X-Requested-With':'XMLHttpRequest',
    "x-xsrf-token": 'b69e1d'
 }

# 保存图片到本地
def save_image(img_src, id, pid,x):
    print(img_src)
    print('\n')
    path = str('web/'+star_id+'/img')
    if not os.path.exists(path):
        os.makedirs(path)
    _name = path+'/' +str(id)+'_' +str(x)+'_'+str(pid) + '.jpg'
    print(_name)
    urllib.request.urlretrieve(img_src, _name)

# 保存 since_id 到 record.text 文件内
def save_record(id):
    if not os.path.exists(str('web/'+star_id)):
        os.makedirs(str('web/'+star_id))
    file = open(str('web/'+star_id+'/record.text'),mode='a')
    if id != '':
        file.write('since_id:'+str(id))
        file.write('\n')
    file.close()

# 获取当前页的微博图片数据
def get_cur_page_weibo(_json,i):
    _cards = _json['data']['cards']
    # _cardListInfo = _json['data']['cardlistInfo']
    # 打印微博
    for card in _cards:
        # 微博
        if card['card_type'] == 9:
            # 只爬取原创微博的配图
            if 'pics' in card['mblog'].keys() and card['mblog']['pics']:
                print(card['mblog']['pic_num'])
                for x in range(len(card['mblog']['pics'])):
                    # 每下载五张图片，休眠 1S
                    if x % 5 == 0:
                        time.sleep(1)
                    print(card['mblog']['pics'][x])
                    save_image(card['mblog']['pics'][x]['large']['url'],card['mblog']['id'],card['mblog']['mid'],x)

# 获取总的图片数量
def get_total_page(_url):
    _response = requests.get(_url, headers=headers)
    print(_response.url)
    _html = _response.text
    __json = json.loads(_html)
    return __json['data']['cardlistInfo']['total']  # 你要爬取的微博的页数

# 总页数
page_total = int(get_total_page(_url))
# since_id
since_id = input_since_id or ""

# 遍历每一页
for i in range(1, page_total):
    headers['Cookie'] = cookie
    __url = _url
    if i > 1 or since_id != '':
        __url = _url+'&since_id='+ str(since_id)
        # print(_url)
    response = requests.get(__url, headers=headers)
    print(response.url)
    html = response.text
    _json = json.loads(html)
    # print(_json['data'])
    if  _json["data"] and _json["data"]["cardlistInfo"] and 'since_id' in _json["data"]["cardlistInfo"]:
        since_id = _json["data"]["cardlistInfo"]["since_id"] or ""
        save_record(since_id)     
    else:
        since_id = ""
        
    if 'cards' in _json['data'] and len(_json['data']['cards']) > 0:
        print(len(_json['data']['cards']))
        # 爬十页休眠5秒
        if i % 10 == 0:
            time.sleep(5)
        else:
            time.sleep(1)
        print("获取当前页面数据----")
        get_cur_page_weibo(_json, i)
    else:
        print('爬取完毕')
        break
