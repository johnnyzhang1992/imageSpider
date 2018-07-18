# !/usr/bin/python
# encoding:utf-8
# 这个例子是去获取微博里的图片，例子爬取的微博是萌妹子吴倩：吴倩mine4ever

# from selenium import webdriver
import time
import requests
import urllib.request
import json
# from bs4 import BeautifulSoup
import os
import sys
import psycopg2
from fake_useragent import UserAgent

ua = UserAgent()
request_params = {"ajwvr":"6","domain":"100505","domain_op":"100505","feed_type":"0","is_all":"1","is_tag":"0","is_search":"0"}
profile_request_params = {"profile_ftype":"1","is_all":"1"}

weibo_url = "https://m.weibo.cn/"
# WEIBO_SECOND_PROFILE_WEIBO 全部
# WEIBO_SECOND_PROFILE_WEIBO_ORI 原创
# WEIBO_SECOND_PROFILE_WEIBO_VIDEO 视频
# WEIBO_SECOND_PROFILE_WEIBO_ARTICAL 文章
# WEIBO_SECOND_PROFILE_WEIBO_WEIBO_SECOND_PROFILE_WEIBO_PIC 文章

star_id = 1

weibo_type = 'WEIBO_SECOND_PROFILE_WEIBO_PIC'

# 数据库
db_name = 'starimg'
db_user = 'postgres'
db_password = input('请输入数据库密码：')

# 时间
created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
updated_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 获取
def get_wb_id(_star_id):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
                            port="5432")
    if conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id,wb_id,name from star WHERE  id = '" + _star_id + "'")
        rows = cur.fetchall()
        if len(rows) > 0:
            print(rows[0][0], rows[0][1],rows[0][2])
            if rows[0][1]:
                return rows[0][1]
        else:
            return 0
    else:
        return 0


def save_image(img_src,id,pid,i):
    print(img_src)
    print('\n')
    if not os.path.exists(str(user_id)):
        os.makedirs(str(user_id))
    _name = str(user_id) + '/' +str(id)+'_'+str(i)+'_' +str(pid) + '.jpg'
    print(_name)
    urllib.request.urlretrieve(img_src, _name)

# 判断是否已入库
def is_in(code,mid,_pid):
    conn1 = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
									 port="5432")
    if conn1:
        cur1 = conn1.cursor()
        cur1.execute("SELECT star_id, code ,mid ,pid from star_img WHERE pid = '"+_pid+"'")
        rows1 = cur1.fetchall()
        if len(rows1) > 0:
            print(rows1[0][0], rows1[0][1], rows1[0][2])
            print('--暂无更新--')
            conn1.commit()
            conn1.close()
            # sys.exit()
            return True
        else:
            conn1.commit()
            conn1.close()
            return  False
    else:
        return False


def insert_database(card,pic,_user_id):
    attitudes_count = card['attitudes_count']
    comments_count = card['comments_count']
    reposts_count = card['reposts_count']
    is_long_text = card['isLongText']
    text = card['text']
    mid = card['mid']
    code = card['bid']
    # 判断是否已入库
    pid = pic['pid']
    if not is_in(code,mid,pid):
        display_url = pic['large']['url']
        pic_detail = pic
        take_at_timestamp = card['created_at']
        source = card['source']
        status = 'active'
        origin_url = 'https://weibo.com/' + _user_id + '/' + code
        print(star_id, '微博', attitudes_count, comments_count, reposts_count, is_long_text, text, mid, code, display_url)
        print(pic_detail)
        print(take_at_timestamp, status)
        conn1 = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
                                 port="5432")
        if conn1:
            cur1 = conn1.cursor()
            cur1.execute("INSERT INTO star_img (star_id,origin,attitudes_count,comments_count,reposts_count,\
                                                                    is_long_text,text,mid,code,display_url,pic_detail,take_at_timestamp,status,created_at,updated_at,origin_url,source,pid) \
                                                                                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                         (star_id, '微博', attitudes_count, comments_count, reposts_count, is_long_text, text, mid,
                          code, display_url, json.dumps(pic_detail), take_at_timestamp, status, created_at, updated_at,
                          origin_url, source,pid))
            conn1.commit()
            conn1.close()
            return True
        else:
            conn1.commit()
            conn1.close()
            return False
    else:
        return False



def get_cur_page_weibo(_json,i,_wb_id):
    _cards = _json['data']['cards']
    # 打印微博
    for card in _cards:
        # 微博
        if card['card_type'] == 9:
            # 只爬取原创微博的配图
            if 'weibo_position' in card['mblog'].keys() and card['mblog']['weibo_position'] == 1:
                if 'pics' in card['mblog'].keys() and card['mblog']['pics']:
                    for x in range(len(card['mblog']['pics'])):
                        # print(card['mblog']['created_at'])
                        if not insert_database(card['mblog'],card['mblog']['pics'][x],_wb_id):
                            continue


def get_total_page(_url,_headers):
    _response = requests.get(_url, headers=_headers)
    # print(_response.url)
    _html = _response.text
    __json = json.loads(_html)
    return  __json['data']['cardlistInfo']['total']  # 你要爬取的微博的页数

def update_wb(_star_id):
    # 判断数据库是否存在wb_id
    wb_id = get_wb_id(_star_id)
    # 更新全局
    global  star_id
    star_id = _star_id
    if wb_id:
        # 字段拼接
        containerid = '230413' + str(wb_id)
        lfid = '230283' + str(wb_id)
        print('---存在wb_id---继续进行')
    else:
        # global user_id
        return False

    _url = 'https://m.weibo.cn/api/container/getIndex?containerid=' + containerid + '_-_' + weibo_type + '&luicode=10000011&lfid=' + lfid

    cookie = '_T_WM=47ce00ce9baf7730b2dee7a7023362d4; SCF=AlD_D4IMYnW7WzQ9VEjiEVe50R9Fshf46k1BIJCyCzJFbuSNTxjfHAv7agK3y3i_9kRG0lCTLIb-91euITt8yQc.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh_3rJYUVcA77DsgIS-UzV_5JpX5K-hUgL.FozXS0Mp1he0eKe2dJLoIEXLxK-LBo5L12qLxK-LBo5L12qLxKqLBKzLBKqLxK-LBoMLBK-LxK-L1-eLB.2t; OUTFOX_SEARCH_USER_ID_NCOO=1522352563.9397414; SUHB=0FQ7BzCGxmtbxL; H5_INDEX_TITLE=%E5%A5%BD%E5%8F%8B%E5%9C%88%20; H5_INDEX=2; ___rl__test__cookies=1526289390542; SUB=_2AkMtpetVdcNxrABTmPgQymPlZIxH-jyecIKjAn7oJhMyPRh77g0AqSdutBF-XJf10Iac9sti1kbQHWAgNUxtA8MZ; MLOGIN=0; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302831900698023%26fid%3D2304131900698023_-_WEIBO_SECOND_PROFILE_WEIBO_PIC%26uicode%3D10000011'
    # User-Agent需要根据每个人的电脑来修改
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'm.weibo.cn',
        'Pragma': 'no-cache',
        'Referer': _url,
        'User-Agent': ua.random,
        'X-Requested-With': 'XMLHttpRequest'
    }
    # 总页数
    page_total = int(get_total_page(_url,headers))
    # 遍历每一页
    for i in range(1, page_total):
        headers['Cookie'] = cookie
        __url = _url
        if i > 1:
            __url = _url + '&page_type=03&page=' + str(i)
            # print(_url)
        response = requests.get(__url, headers=headers)
        # print(response.url)
        html = response.text
        _json = json.loads(html)
        if 'cards' in _json['data'] and len(_json['data']['cards']) > 0:
            # 爬十页休眠5秒
            if i % 10 == 0:
                time.sleep(5)
            time.sleep(1)
            if not get_cur_page_weibo(_json, i,wb_id):
                return False
            else:
                return True
        else:
            print('爬取完毕')
            return False


conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
									 port="5432")
if conn:
    cur = conn.cursor()
    cur.execute(
        "SELECT id, wb_id,name from star ORDER BY id ASC ")
    rows = cur.fetchall()
    # print(rows)
    # print(len(rows))
    conn.commit()
    conn.close()
    if len(rows) > 0:
        for n in range(len(rows)):
            print(str(rows[n][0]),rows[n][1],rows[n][2])
            if not update_wb(str(rows[n][0])):
                continue
            # sys.exit()

