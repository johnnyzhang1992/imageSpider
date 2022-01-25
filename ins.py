# !/usr/bin/python
# encoding:utf-8
# 这个例子是去获取ins里的图片，因为墙，所以爬的是一个国内的站

# from selenium import webdriver
import time
import math
import requests
# import urllib.request
import json
from bs4 import BeautifulSoup
import os
import sys
import psycopg2
from fake_useragent import UserAgent

ua = UserAgent()
request_params = {"ajwvr":"6","domain":"100505","domain_op":"100505","feed_type":"0","is_all":"1","is_tag":"0","is_search":"0"}
profile_request_params = {"profile_ftype":"1","is_all":"1"}

ins_url = "https://www.veryins.com"

# 林允儿
# user_id = 'yoona__lim'
# user_id = input('请输入所要爬取的用户username:')
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
if user_id:
    print('---存在wb_id---继续进行')
else:
    # global user_id
    user_id = input('请输入所要爬取的用户id:')

# 拼接
_url = ins_url+'/'+str(user_id)
start_cookie_id = 1544684329
_cookie = '__cfduid=d765bdd1608f3e9bc972e1a189fdf1b381540347408; ___rl__test__cookies=1542681514842; OUTFOX_SEARCH_USER_ID_NCOO=1029395707.9778699;' \
          ' Hm_lvt_453ab3ca06e82d916be6d6937c3bf101=1543893599,1544433571,1544665231,1544665483; ' \
          'hd_hongbao=1; connect.sid=s%3As9xLGPi5xWnimSLCI4R9Nqae7i4qdCvO.nHwB9Ledau5cPSUEP%2Bl1ba1ky6ZMXo%2BQ6u1cQi%2BPn1c;' \
          ' Hm_lpvt_453ab3ca06e82d916be6d6937c3bf101='
cookie = _cookie + str(start_cookie_id)
# User-Agent需要根据每个人的电脑来修改
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
	'Connection':'keep-alive',
	# 'Content-Type':'application/x-www-form-urlencoded',
	'Host':'www.veryins.com',
	'Pragma':'no-cache',
	'Cookie': cookie,
    # 'Upgrade - Insecure - Requests': '1',
    # 'User-Agent':ua.random
 }

# 是否有下一页
has_next_page = True

result = requests.Session()

# 抓取首屏信息，获得用户的id以及下一页加载的next_cursor
req = result.get(_url, headers=headers)
print('status code: '+str(req.status_code))
# print(req.text)
if req.status_code == 200:
    print('页面抓取正常')
elif req.status_code == 404:
    print('当前用户不存在')
    # 退出程序
    sys.exit()
else:
    print('页面抓取异常')
    print(req.text)
    print(req.status_code)

# 时间
created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
updated_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

soup = BeautifulSoup(req.text, 'html.parser')

# uid 用户id
_uid = soup.find(id='username')
_uid = _uid.attrs['data-uid']

# 加载下一页的凭证
_list = soup.find(id='list')
next_cursor = _list.attrs['next-cursor']
rg = _list.attrs['data-rg']
# next_cursor = 'AQC868BPpK36PCrdlgAiCXEVKO5a3UgzROOSpKoaJdaDbYBwwWWS7KlRgUhZAvc9vnYb0W5EpLfeX6wS6XgbcNH4dsqpJ183nms8lYjEAfVLpg'
# _uid = '652770539'
# rg = '79a7de060d56c4d4a259ecce65bbfd1c'
# 当前用户的 ins 总条数
total = 544

current_page = 0

# 数据获取方式
# 第一步，获取 p 元素的 code
# 第二部，根据 code 获取图片或者视频的详细信息


# 用户第一页内容
def get_first_page_data(_soup):
    print('---第一页数据')
    items = _soup.find_all('div',class_='item')
    if int(len(items)) > 0:
        print('items-length:' + str(len(items)))
        for i in range(0, int(len(items))):
            _item = items[i].find('div', attrs={'class': 'img-wrap'})
            print(_item.attrs['data-code'])
            _like = items[i].find('div', attrs={'class': 'likes'})
            _like = _like.find('span', attrs={'class': 'h6'})
            _like = _like.get_text()
            if not is_in(_item.attrs['data-code']):
                return False
            else:
                get_p_info(_item.attrs['data-code'], _like)
    else:
        print('当前用户无公开内容')


# 获取下一页内容
def get_next_data(_next_cursor, _rg, _has_next_page, __uid):
    print(_next_cursor,_rg,_has_next_page,__uid)
    if _next_cursor != '' and _has_next_page:
        __url = ins_url + '/user/' + user_id + '?next=' + _next_cursor + '&uid=' + __uid + '&rg=' + _rg
        print(__url)
        # 更新请求头
        __ua = UserAgent()
        headers['Referer'] = ins_url + '/' + user_id
        headers['Accept'] = '*/*'
        headers['Content-Length'] = '0'
        headers['Host'] = 'www.veryins.com'
        headers['Origin'] = ins_url
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['User-Agent'] = __ua.random
        # print(headers)
        response = requests.post(__url, headers=headers)
        if response.status_code == 200:
            print('页面抓取正常')
        elif response.status_code == 404:
            print('当前页面不存在')
            # 退出程序
            sys.exit()
        else:
            print('页面抓取异常')
            print(response.headers)
            sys.exit()
        # 获得的 json 格式的 ins 内容，先解析
        _json = json.loads(response.text)
        # print(_json)
        # 更新全局的下一页凭证以及是否存在下一页
        global next_cursor
        global has_next_page
        next_cursor = _json['user']['media']['page_info']['end_cursor']
        has_next_page = _json['user']['media']['page_info']['has_next_page']
        print(next_cursor, has_next_page)
        # 遍历 json ，通过里面的单条ins的变识码，获取其详细信息
        if len(_json['user']['media']['nodes']) > 0:
            for i in range(0, int(len(_json['user']['media']['nodes']))):
                # code
                print(_json['user']['media']['nodes'][i]['code'])
                # 获取当前页面的所有单条内容的详细信息
                if not get_p_info(_json['user']['media']['nodes'][i]['code'],
                                  _json['user']['media']['nodes'][i]['likes']):
                    continue


# 获取第二页的内容
def get_second_page_data(_next_cursor, _rg, _has_next_page, __uid):
    print('second page')
    print(_next_cursor, _rg, _has_next_page, __uid)
    if _next_cursor != '' and _has_next_page:
        __url = ins_url + '/user/' + user_id + '?next=' + _next_cursor + '&uid=' + __uid + '&rg=' + _rg
        print(__url)
        # 更新请求头
        headers['Referer'] = ins_url + '/' + user_id
        headers['Accept'] = '*/*'
        headers['Content-Length'] = '0'
        headers['Host'] = 'www.veryins.com'
        headers['Origin'] = ins_url
        global start_cookie_id
        _ua = UserAgent()
        start_cookie_id = start_cookie_id
        headers['Cookie'] = _cookie + str(start_cookie_id)
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['User-Agent'] = _ua.random
        # headers[
            # 'User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        # print(headers)
        response = result.post(__url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            print('页面抓取正常')
        elif response.status_code == 404:
            print('当前页面不存在')
            # 退出程序
            sys.exit()
        else:
            print('页面抓取异常')
            # print(response)
            # print(response.text)
            print(response.headers)
            sys.exit()
        # 获得的 json 格式的 ins 内容，先解析
        _json = json.loads(response.text)
        # 更新全局的下一页凭证以及是否存在下一页
        global total
        global next_cursor
        global has_next_page
        # ins 总条数，用来计算总页数
        total = _json['user']['media']['count']
        next_cursor = _json['user']['media']['page_info']['end_cursor']
        has_next_page = _json['user']['media']['page_info']['has_next_page']
        print('total:' + str(total))
        print('total_page:' + str(math.ceil(total / 12)))
        # 遍历 json ，通过里面的单条ins的变识码，获取其详细信息
        if len(_json['user']['media']['nodes']) > 0:
            for i in range(0, int(len(_json['user']['media']['nodes']))):
                # code
                print(_json['user']['media']['nodes'][i]['code'])
                # 获取当前页面的所有单条内容的详细信息
                if not get_p_info(_json['user']['media']['nodes'][i]['code'],
                                  _json['user']['media']['nodes'][i]['likes']):
                    continue


# 判断是否已入库
def is_in(code):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
                            port="5432")
    if conn:
        cur = conn.cursor()
        # cur.execute("SELECT star_id, code from star_img WHERE status
        # = 'active' AND code = '" + code + "' AND star_id = '"+ star_id+"'")
        cur.execute("SELECT star_id, code from star_img WHERE code = '" + code + "' AND star_id = '" + star_id + "'")

        rows = cur.fetchall()
        if len(rows) > 0:
            print(rows[0][0], rows[0][1])
            conn.commit()
            conn.close()
            return False
        else:
            return True
    else:
        return True


# 获取单条内容的详细信息
def get_p_info(_code,_like):
    # if current_page<16:
    # 	print('current_page'+str(current_page))
    # 	return  False
    # 判断是否已经入库
    if not is_in(_code):
        return False
    else:
        # 更新请求头
        _ua = UserAgent()
        headers['Referer'] = ins_url + '/p/' + _code
        headers['Accept'] = '*/*'
        headers['Content-Length'] = '0'
        headers['Host'] = 'www.veryins.com'
        headers['Origin'] = ins_url
        global start_cookie_id
        start_cookie_id = start_cookie_id + 1
        headers['Cookie'] = _cookie + str(start_cookie_id)
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['User-Agent'] = _ua.random
        __url = ins_url + '/p/' + _code
        time.sleep(1)
        response = requests.post(__url, headers=headers)
        if response.status_code == 200:
            print('页面抓取正常')
        elif response.status_code == 404:
            print('当前页面不存在')
            # 退出程序
            return False
        else:
            print('页面抓取异常')
            print(response.headers)
            return False
        # 获得此条 ins 的详细信息，解析处理后待入库
        if response.text and response.text != '':
            _json = json.loads(response.text)
            display_url = _json['display_url']
            take_at_timestamp = _json['taken_at_timestamp']
            attitudes_count = _like
            pic_detail = _json['display_resources']
            is_video = _json['is_video']
            video_url = _json['video_url']
            status = 'active'
            if 'caption' in _json.keys():
                text = _json['caption']
            else:
                text = ''
            origin_url = 'https://www.veryins.com/p/' + _code
            print('Instagram', display_url, take_at_timestamp, attitudes_count, is_video, video_url)
            # print(pic_detail)
            if _json['sidecar'] and len(_json['sidecar']) > 0:
                for i in range(0, len(_json['sidecar'])):
                    pic_detail = None
                    display_url = _json['sidecar'][i]['display_url']
                    print(pic_detail, display_url)
                    conn2 = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
                                             port="5432")
                    if conn2:
                        cur1 = conn2.cursor()
                        cur1.execute("INSERT INTO star_img (star_id,origin,attitudes_count,text,code,display_url,pic_detail,take_at_timestamp,is_video,video_url,status,created_at,updated_at,origin_url) \
            	    				                                                                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                     (star_id, 'instagram', attitudes_count, text,
                                      _code, display_url, json.dumps(pic_detail), take_at_timestamp, is_video,
                                      video_url,
                                      status, created_at, updated_at,
                                      origin_url))
                        conn2.commit()
                        conn2.close()
                        time.sleep(1)
                    else:
                        conn2.close()
            else:
                conn1 = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
                                         port="5432")
                if conn1:
                    cur1 = conn1.cursor()
                    cur1.execute("INSERT INTO star_img (star_id,origin,attitudes_count,text,code,display_url,\
                                     pic_detail,take_at_timestamp,is_video,video_url,status,created_at,updated_at,origin_url) \
                                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 (star_id, 'instagram', attitudes_count, text,
                                  _code, display_url, json.dumps(pic_detail), take_at_timestamp, is_video, video_url,
                                  status,
                                  created_at, updated_at,
                                  origin_url))
                    conn1.commit()
                conn1.close()
        return True


# 第一页内容
get_first_page_data(soup)
# 第二页内容
get_second_page_data(next_cursor, rg, has_next_page, _uid)


# 从第三页以及剩余的内容

for i in range(1, int(math.ceil(total / 12)-1)):
    print('current_page: '+str(i+2))

    # global current_page
    # current_page = i+2
    # print(i)

    time.sleep(3)
    if i % 4 == 0:
        print('---休眠15秒--')
        time.sleep(15)
    if i % 10 == 0:
        print('---休眠30秒')
        time.sleep(30)
    if has_next_page:
        # 获取下一页的 ins 内容
        get_next_data(next_cursor, rg, has_next_page, _uid)
