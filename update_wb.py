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


# def save_image(img_src,id,pid,i):
#     print(img_src)
#     print('\n')
#     if not os.path.exists(str(user_id)):
#         os.makedirs(str(user_id))
#     _name = str(user_id) + '/' +str(id)+'_'+str(i)+'_' +str(pid) + '.jpg'
#     print(_name)
#     urllib.request.urlretrieve(img_src, _name)


# 判断是否已入库
def is_in(code,mid,_pid,attitudes_count):
    conn1 = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1", port="5432")
    if conn1:
        cur1 = conn1.cursor()
        cur1.execute("SELECT star_id, code ,mid ,pid from star_img WHERE pid = '"+_pid+"'")
        rows1 = cur1.fetchall()
        if len(rows1) > 0:
            print(rows1[0][0], rows1[0][1], rows1[0][2])
            print('--暂无更新--')
            cur1.execute("UPDATE star_img  set attitudes_count = '" + str(attitudes_count) + "' WHERE pid = '"+str(_pid)+"' ")
            conn1.commit()
            conn1.close()
            print('---更新点赞数--'+ str(attitudes_count))
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
    if not is_in(code, mid, pid,attitudes_count):
        display_url = pic['large']['url']
        pic_detail = pic
        take_at_timestamp = card['created_at']
        source = card['source']
        status = 'active'
        origin_url = 'https://weibo.com/' + _user_id + '/' + code
        print(star_id, '微博', attitudes_count, comments_count, reposts_count, is_long_text, text, mid, code, display_url)

        print(pic_detail)
        print(take_at_timestamp, status)
        conn1 = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1", port="5432")
        if str(attitudes_count).find('万+') >= 0:
            attitudes_count = int(attitudes_count.replace("万+", "0000"))
        if str(comments_count).find('万+') >= 0:
            comments_count = int(comments_count.replace("万+", "0000"))
        if str(reposts_count).find('万+') >= 0:
            reposts_count = int(reposts_count.replace("万+", "0000"))
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


def get_cur_page_weibo(_json, i, _wb_id):
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


def get_total_page(_url, _headers):
    print(_url)
    # 2秒休眠
    time.sleep(2)
    _response = requests.get(_url, headers=_headers)
    # print(_response.url)
    _html = _response.text
    __json = json.loads(_html)
    if __json['data'] and __json['data']['cardlistInfo']:
        return __json['data']['cardlistInfo']['total']  # 你要爬取的微博的页数
    else:
        return False


def update_wb(_star_id):
    # 判断数据库是否存在wb_id
    wb_id = get_wb_id(_star_id)
    # 更新全局
    global star_id
    star_id = _star_id
    if wb_id:
        # 字段拼接
        containerid = '230413' + str(wb_id)
        lfid = '230283' + str(wb_id)
        print('---存在wb_id---继续进行')
    else:
        # global user_id
        return 1

    _url = 'https://m.weibo.cn/api/container/getIndex?containerid=' + containerid + '_-_' + weibo_type + '&luicode=10000011&lfid=' + lfid

    cookie = 'WEIBOCN_FROM=1110003030; OUTFOX_SEARCH_USER_ID_NCOO=123636308.59677954; SCF=AhTMNl9bAeJagBTL5WGe7GNzjCkO383UWVTXYQT7GOZl_moFcko7o_e4THpdktKfDvh_so5KnHRtQmyCQgv0IyQ.; SUHB=0QS5d_Aa7-wF5m; _T_WM=08780ade7cbb594bc7f80e940f617a83; SSOLoginState=1548123454; ALF=1550715454; MLOGIN=0; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302831246229612%26fid%3D2304131246229612_-_WEIBO_SECOND_PROFILE_WEIBO_PIC%26uicode%3D10000011'
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
    page_total = int(get_total_page(_url, headers))
    # 遍历每一页
    for i in range(1, page_total):
        headers['Cookie'] = cookie
        headers['User-Agent'] = ua.random
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
            if not get_cur_page_weibo(_json, i, wb_id):
                return False
            else:
                return True
        else:
            print('爬取完毕')
            return False


conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1", port="5432")
if conn:
    cur = conn.cursor()
    cur.execute(
        "SELECT id, wb_id,name from star WHERE status = 'active' ORDER BY id ASC ")
    rows = cur.fetchall()
    # print(rows)
    # print(len(rows))
    conn.commit()
    conn.close()
    if len(rows) > 0:
        for n in range(len(rows)):
            # 爬10个用户休眠5秒
            if n > 10 and n % 10 == 0:
                time.sleep(10)
                print('休眠10秒')
            time.sleep(3)
            print('休眠3秒')
            print(str(rows[n][0]), rows[n][1], rows[n][2])
            if not update_wb(str(rows[n][0])):
                continue
            # sys.exit()

