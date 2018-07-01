# !/usr/bin/python
# encoding:utf-8
# 这个例子是去获取微博里的图片，例子爬取的微博是萌妹子吴倩：吴倩mine4ever

# from selenium import webdriver
import time
import requests
# import urllib.request
import json
# from bs4 import BeautifulSoup
import psycopg2
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

# user_id = '1900698023'
# user_id = input('请输入所要爬取的用户id:')
star_id = input('请输入star_id:')
# star_id = int(star_id)

# 数据库
db_name = 'starimg'
db_user = 'postgres'
db_password = input('请输入数据库密码：')

# 获取
def get_wb_id(_star_id):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
                            port="5432")
    if conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id,wb_id from star WHERE  id = '" + _star_id + "'")
        rows = cur.fetchall()
        if len(rows) > 0:
            print(rows[0][0], rows[0][1])
            if rows[0][1]:
                return rows[0][1]
        else:
            return False
    else:
        return False


# 判断数据库是否存在wb_id
user_id = get_wb_id(star_id)
if  user_id:
    print('---存在wb_id---继续进行')
else:
    # global user_id
    user_id = input('请输入所要爬取的用户id:')

# 拼接字段
weibo_type = 'WEIBO_SECOND_PROFILE_WEIBO_PIC'
containerid = '230413'+user_id
lfid = '230283'+user_id

_url = 'https://m.weibo.cn/api/container/getIndex?containerid='+ containerid+'_-_'+weibo_type+'&luicode=10000011&lfid='+lfid+'&type=uid&value='+user_id

cookie = 'OUTFOX_SEARCH_USER_ID_NCOO=200622491.85643607; _T_WM=5fe554ab8cacafd1178a525cdecf9e27; ALF=1532570144; WEIBOCN_FROM=1110006030; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh_3rJYUVcA77DsgIS-UzV_5JpX5K-hUgL.FozXS0Mp1he0eKe2dJLoIEXLxK-LBo5L12qLxK-LBo5L12qLxKqLBKzLBKqLxK-LBoMLBK-LxK-L1-eLB.2t; MLOGIN=1; SCF=AlD_D4IMYnW7WzQ9VEjiEVe50R9Fshf46k1BIJCyCzJFNXp5Ai-xhaJMvwpW7jxV361LEmg8knsQ7H0vcFYg1nI.; SUB=_2A252Nbk8DeRhGeRK7FUQ-C3Pyj-IHXVV2cd0rDV6PUJbktAKLWv_kW1NUyw6NHG_SIkq3ybyx2AupZO4pWVE13rr; SUHB=0BLpnRWl2XCpLH; SSOLoginState=1529989484; M_WEIBOCN_PARAMS=oid%3D2304131350995007_-_WEIBO_SECOND_PROFILE_MORE_WEIBO%26fid%3D2302831350995007%26luicode%3D10000011%26lfid%3D2302831350995007%26uicode%3D10000011'
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
	'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
 }


star_info = ''
# 明星信息
def get_user_info(user):
    global  star_info
    print('--get-user-info---')
    star_info = user
    # print(user)
    return  user

# 根据输入的star_id判断数据库中是否存在改star
def is_has_star():
    _conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",port="5432")
    if _conn:
        cur = _conn.cursor()
        cur.execute("SELECT id, name from star WHERE id = '" + star_id + "'")
        rows = cur.fetchall()
        if len(rows) > 0:
            print('用户存在：',rows[0][0], rows[0][1])
            print('\n')
        else:
            print(star_id+'需要先创建star哦\n')
    else:
        print('连接数据库失败\n')


# 判断用户是否存在
is_has_star()
_response = requests.get(_url, headers=headers)
# 抓取首屏信息，获得用户的id以及下一页加载的next_cursor
print('status code: '+str(_response.status_code))

if _response.status_code == 200:
    print('页面抓取正常')
elif _response.status_code == 404:
    print('当前用户不存在')
    # 退出程序
    sys.exit()
else:
    print('页面抓取异常')
    print(_response.headers)

# 抓取页面信息
print(_response.url)
_html = _response.text
_json = json.loads(_html)
_cards = _json['data']['cards']
print(len(_cards))
def save_sql():
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
                            port="5432")
    created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    updated_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(created_at,updated_at)
    if star_info['verified']:
        print(star_info['verified_reason'])
    else:
        star_info['verified_reason'] = '无'
    if conn:
        cur = conn.cursor()
        # 判断是否存在
        cur.execute("SELECT id, screen_name from star_wb WHERE star_id = '" + star_id + "'")
        rows = cur.fetchall()
        # 存在，update
        if len(rows) > 0:
            print('\n')
            print('----用户存在：', rows[0][1])
            print('更新数据中。。。\n')
            cur.execute("UPDATE star_wb \
                set screen_name = '" + star_info['screen_name'] + "',verified = '"+ str(star_info['verified'])+"',\
                 verified_reason = '"+star_info['verified_reason']+"',\
                avatar = '"+star_info['avatar_hd']+"' ,updated_at = '"+updated_at+"'\
                WHERE screen_name ='"+rows[0][1]+"' ")
            conn.commit()
            conn.close()
        else:
            # 不存在，插入
            print('插入数据中。。。\n')
            conn.close()
            conn1 = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
                            port="5432")
            if conn1:
                cur1 = conn1.cursor()
                cur1.execute("INSERT INTO star_wb (star_id,wb_id,screen_name,verified,verified_reason,description,gender,\
                            followers_count,follow_count,avatar,created_at,updated_at) \
                                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                             (star_id, star_info['id'], star_info['screen_name'], star_info['verified'],
                              star_info['verified_reason'],
                              star_info['description'],
                              star_info['gender'],
                              star_info['followers_count'], star_info['follow_count'], star_info['avatar_hd'],
                              created_at, updated_at))

                conn1.commit()
                conn1.close()
    else:
        conn.close()

# 打印微博
for card in _cards:
    # 微博
    if card['card_type'] == 9:
        # 只爬取原创微博的配图
        if card['mblog']:
               if card['mblog']['weibo_position'] == 1:
                print('----user--')
                get_user_info(card['mblog']['user'])
                save_sql()
                break
        else:
            continue
    else:
        continue


