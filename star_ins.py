# !/usr/bin/python
# encoding:utf-8
# 这个例子是去获取ins里的图片，因为墙，所以爬的是一个国内的站

# from selenium import webdriver
import time
import math
import requests
# import urllib.request
# import json
from bs4 import BeautifulSoup
import os
import psycopg2
import sys

request_params = {"ajwvr":"6","domain":"100505","domain_op":"100505","feed_type":"0","is_all":"1","is_tag":"0","is_search":"0"}
profile_request_params = {"profile_ftype":"1","is_all":"1"}

ins_url = "http://www.insstar.cn"

# 林允儿
# user_id = 'yoona__lim'
# user_id = input('请输入所要爬取的用户username:')

# star_id:
star_id = input('请输入star_id:')

# 数据库
db_name = 'starimg'
db_user = 'postgres'
db_password = input('请输入数据库密码：')

# 获取
def get_ins_name(_star_id):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
                            port="5432")
    if conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id,ins_name from star WHERE  id = '" + _star_id + "'")
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
user_id = get_ins_name(star_id)
if  user_id:
    print('---存在wb_id---继续进行')
else:
    # global user_id
    user_id = input('请输入所要爬取的用户user_name:')

# 拼接
_url = ins_url+'/'+str(user_id)
#gender
gender = input('性别(f/m):')

cookie = 'OUTFOX_SEARCH_USER_ID_NCOO=1467016326.6141114; connect.sid=s%3Abd7AuHfrAsq0x0PnwvKWawv_WyGIoyJb.6OtWC%2BNE33fJXfKvQuoM4WTHDAEjb3IsN9JpZ77dJG8; Hm_lvt_f9dcf4433e76d7f5b041b0634f78a43a=1526376660,1526396423,1526552953,1526565679; Hm_lpvt_f9dcf4433e76d7f5b041b0634f78a43a=1526565679'

# User-Agent需要根据每个人的电脑来修改
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
	'Connection':'keep-alive',
	# 'Content-Type':'application/x-www-form-urlencoded',
	'Host':'www.insstar.cn',
	'Pragma':'no-cache',
	'Cookie': cookie,
    'Upgrade - Insecure - Requests': '1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
 }

# 是否有下一页
has_next_page = True

# 抓取首屏信息，获得用户的id以及下一页加载的next_cursor
req = requests.get(_url, headers=headers)
print('status code: '+str(req.status_code))

if req.status_code == 200:
	print('页面抓取正常')
elif req.status_code == 404:
	print('当前用户不存在')
	# 退出程序
	sys.exit()
else:
	print('页面抓取异常')
	print(req.headers)

soup = BeautifulSoup(req.text, 'html.parser')

# uid 用户id
_uid = soup.find(id='username')
_uid = _uid.attrs['data-uid']
# 是否认证
_is_verified = soup.find_all('img', attrs={'class': 'verified'})
is_verified = False
if len(_is_verified) > 0 :
    is_verified = True

# 粉丝和关注数量
followers_count = 0
follow_count = 0
_count = soup.find('ul',attrs={'class':'count'})
_count_li = _count.find_all('li')
if len(_count_li)>0:
    for i in range(0,len(_count_li)):
        # global follow_count
        # global followers_count
        if i ==1:
            follow_count = _count_li[i].find('strong').get_text()
        elif i == 2:
            followers_count = _count_li[i].find('strong').get_text()
# 介绍
_desc = soup.find('p',attrs={'class':'biography'})
description = _desc.get_text()
# 头像
_avatar = soup.find('img',attrs={'class':'avatar'})
avatar = _avatar.attrs['src']
# 时间
created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
updated_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
                            port="5432")
print('是否认证：'+ str(is_verified))
print('粉丝：'+followers_count)
print('关注：'+follow_count)
print('介绍：'+description)
print('头像：'+avatar)
print(created_at,updated_at)
if conn:
    cur = conn.cursor()
    # 判断是否存在
    cur.execute("SELECT id, name from star_ins WHERE star_id = '" + star_id + "'")
    rows = cur.fetchall()
    # 存在，update
    if len(rows) > 0:
        print('\n')
        print('用户存在：', rows[0][1])
        print('更新数据中。。。\n')
        cur.execute("UPDATE star_ins set name = '" + user_id+ "',verified = '" + str(
            is_verified) + "',  followers_count = '" + followers_count + "' ,follow_count = '" + follow_count + "',avatar = '" + avatar+ "' ,updated_at = '" + updated_at + "'\
                         WHERE name ='" + rows[0][1] + "' ")
        # cur.execute("UPDATE author set more_infos = '" + _content_json + "' where source_id='" + str(_id) + "'")
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
            cur1.execute("INSERT INTO star_ins (star_id,ins_id,name,verified,description,gender,\
                                     followers_count,follow_count,avatar,created_at,updated_at) \
                                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                         (star_id, _uid, user_id, is_verified,
                          description,gender,followers_count, follow_count, avatar,
                          created_at, updated_at))

            conn1.commit()
            conn1.close()
        else:
            conn.close()