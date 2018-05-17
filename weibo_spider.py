# !/usr/bin/python
# encoding:utf-8
# 这个例子是去获取微博里的图片，例子爬取的微博是萌妹子吴倩：吴倩mine4ever

from selenium import webdriver
import time
import requests
import urllib.request
import json
from bs4 import BeautifulSoup
import os
import sys

request_params = {"ajwvr":"6","domain":"100505","domain_op":"100505","feed_type":"0","is_all":"1","is_tag":"0","is_search":"0"}
profile_request_params = {"profile_ftype":"1","is_all":"1"}

weibo_url = "https://m.weibo.cn/"
# WEIBO_SECOND_PROFILE_WEIBO 全部
# WEIBO_SECOND_PROFILE_WEIBO_ORI 原创
# WEIBO_SECOND_PROFILE_WEIBO_VIDEO 视频
# WEIBO_SECOND_PROFILE_WEIBO_ARTICAL 文章
# WEIBO_SECOND_PROFILE_WEIBO_WEIBO_SECOND_PROFILE_WEIBO_PIC 文章

cookie_save_file = "cookie.txt"#存cookie的文件名
cookie_update_time_file = "cookie_timestamp.txt"#存cookie时间戳的文件名
image_result_file = "image_result.md"#存图片结果的文件名

user_id = '1900698023'
weibo_type = 'WEIBO_SECOND_PROFILE_WEIBO_PIC'
containerid = '230413'+user_id
lfid = '230283'+user_id
# username = 'your weibo accounts'##你的微博账号
# password = 'your weibo password'##你的微博密码

_url = 'https://m.weibo.cn/api/container/getIndex?containerid='+ containerid+'_-_'+weibo_type+'&luicode=10000011&lfid='+lfid

cookie = '_T_WM=47ce00ce9baf7730b2dee7a7023362d4; SCF=AlD_D4IMYnW7WzQ9VEjiEVe50R9Fshf46k1BIJCyCzJFbuSNTxjfHAv7agK3y3i_9kRG0lCTLIb-91euITt8yQc.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh_3rJYUVcA77DsgIS-UzV_5JpX5K-hUgL.FozXS0Mp1he0eKe2dJLoIEXLxK-LBo5L12qLxK-LBo5L12qLxKqLBKzLBKqLxK-LBoMLBK-LxK-L1-eLB.2t; OUTFOX_SEARCH_USER_ID_NCOO=1522352563.9397414; SUHB=0FQ7BzCGxmtbxL; H5_INDEX_TITLE=%E5%A5%BD%E5%8F%8B%E5%9C%88%20; H5_INDEX=2; ___rl__test__cookies=1526289390542; SUB=_2AkMtpetVdcNxrABTmPgQymPlZIxH-jyecIKjAn7oJhMyPRh77g0AqSdutBF-XJf10Iac9sti1kbQHWAgNUxtA8MZ; MLOGIN=0; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302831900698023%26fid%3D2304131900698023_-_WEIBO_SECOND_PROFILE_WEIBO_PIC%26uicode%3D10000011'
# User-Agent需要根据每个人的电脑来修改
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded',
	'Host':'m.weibo.cn',
	'Pragma':'no-cache',
	'Referer':_url,
	'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
	'X-Requested-With':'XMLHttpRequest'
 }
cur_page = 1
n = 1


def save_image(img_src,id,pid,i):
    print(img_src)
    print('\n')
    if not os.path.exists(str(user_id)):
        os.makedirs(str(user_id))
    _name = str(user_id) + '/' +str(id)+'_'+str(i)+'_' +str(pid) + '.jpg'
    print(_name)
    urllib.request.urlretrieve(img_src, _name)


def get_cur_page_weibo(_json,i):
    _cards = _json['data']['cards']
    _cardListInfo = _json['data']['cardlistInfo']

    page_total = _cardListInfo['total']  # 你要爬取的微博的页数
    cur_page = _cardListInfo['page']  # 当前微博页数
    print(cur_page, page_total)
    # 打印微博
    for card in _cards:
        if card['card_type'] == 9:
            if card['mblog']['weibo_position'] == 1:
                if card['mblog']['pics']:
                    for x in range(len(card['mblog']['pics'])):
                        # print(card['mblog']['pics'][x]['large']['url'])
                        print(card['mblog']['created_at'])
                        save_image(card['mblog']['pics'][x]['large']['url'],card['mblog']['created_at'],x,card['mblog']['mid'])
                        # print(card['mblog'])


def get_total_page(_url):
    _response = requests.get(_url, headers=headers)
    print(_response.url)
    _html = _response.text
    __json = json.loads(_html)
    return  __json['data']['cardlistInfo']['total']  # 你要爬取的微博的页数

page_total = int(get_total_page(_url))
# 遍历每一页
for i in range(1, page_total):
    headers['Cookie'] = cookie
    # print(_url)
    if i > 1:
        _url = _url+'&page_type=03&page='+str(i)
        print(_url)
    response = requests.get(_url, headers=headers)
    print(response.url)
    html = response.text
    _json = json.loads(html)
    get_cur_page_weibo(_json,i)

