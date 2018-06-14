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

ins_url = "http://www.insstar.cn"

# 林允儿
# user_id = 'yoona__lim'
user_id = input('请输入所要爬取的用户username:')
star_id = input('请输入star_id:')
_url = ins_url+'/'+str(user_id)

cookie = 'OUTFOX_SEARCH_USER_ID_NCOO=1467016326.6141114; connect.sid=s%3AdFjfuNVHoWOhMetAMn3AC97MWIOrLbQz.Vusw%2FQByZvSxZzBmFfyl8BuG4jrD%2FfVxEeJBLFcjfyQ; Hm_lvt_f9dcf4433e76d7f5b041b0634f78a43a=1527477805,1527839810,1528004944,1528078892; Hm_lpvt_f9dcf4433e76d7f5b041b0634f78a43a=1528081998'

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
	'User-Agent':ua.random
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
	print(req)
	print(req.status_code)

# 数据库
db_name = 'starimg'
db_user = 'postgres'
db_password = input('请输入数据库密码：')

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
	items = _soup.find_all('div',class_='item')
	if int(len(items)) > 0:
		print('items-length:'+str(len(items)))
		for i in range(0,int(len(items))):
			_item =items[i].find('div',attrs={'class':'img-wrap'})
			print(_item.attrs['data-code'])
			_like = items[i].find('div',attrs={'class':'likes'})
			_like = _like.find('span',attrs={'class':'h6'})
			_like = _like.get_text()
			get_p_info(_item.attrs['data-code'],_like)
	else:
		print('当前用户无公开内容')


# 获取下一页内容
def get_next_data(_next_cursor, _rg, _has_next_page, __uid):
	print(_next_cursor,_rg,_has_next_page,__uid)
	if _next_cursor != '' and _rg != '' and _has_next_page:
		__url = ins_url + '/user/' + user_id + '?next=' + _next_cursor + '&uid=' + __uid + '&rg=' + _rg
		print(__url)
		# 更新请求头
		__ua = UserAgent()
		headers['Referer'] = ins_url+'/'+user_id
		headers['Accept'] = '*/*'
		headers['Content-Length'] = '0'
		headers['Host'] =  'www.insstar.cn'
		headers['Origin'] =ins_url
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
		next_cursor= _json['user']['media']['page_info']['end_cursor']
		has_next_page= _json['user']['media']['page_info']['has_next_page']
		print(next_cursor,has_next_page)
		# 遍历 json ，通过里面的单条ins的变识码，获取其详细信息
		if len(_json['user']['media']['nodes'])>0:
			for i in range(0,int(len(_json['user']['media']['nodes']))):
				# code
				print(_json['user']['media']['nodes'][i]['code'])
				# 获取当前页面的所有单条内容的详细信息
				get_p_info(_json['user']['media']['nodes'][i]['code'],_json['user']['media']['nodes'][i]['likes'])

# 获取第二页的内容
def get_second_page_data(_next_cursor, _rg, _has_next_page, __uid):
	print(_next_cursor, _rg, _has_next_page, __uid)
	if _next_cursor != '' and _rg != '' and _has_next_page:
		__url = ins_url+'/user/'+user_id+'?next=' + _next_cursor + '&uid=' + __uid + '&rg=' + _rg
		print(__url)
		# 更新请求头
		headers['Referer'] = ins_url + '/' + user_id
		headers['Accept'] = '*/*'
		headers['Content-Length'] = '0'
		headers['Host'] = 'www.insstar.cn'
		headers['Origin'] = ins_url
		headers['X-Requested-With'] = 'XMLHttpRequest'
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
		# 更新全局的下一页凭证以及是否存在下一页
		global total
		global next_cursor
		global has_next_page
		# ins 总条数，用来计算总页数
		total= _json['user']['media']['count']
		next_cursor= _json['user']['media']['page_info']['end_cursor']
		has_next_page= _json['user']['media']['page_info']['has_next_page']
		print('total:'+str(total))
		print('total_page:'+str(math.ceil(total / 12)))
		# 遍历 json ，通过里面的单条ins的变识码，获取其详细信息
		if len(_json['user']['media']['nodes'])>0:
			for i in range(0,int(len(_json['user']['media']['nodes']))):
				# code
				print(_json['user']['media']['nodes'][i]['code'])
				# 获取当前页面的所有单条内容的详细信息
				get_p_info(_json['user']['media']['nodes'][i]['code'],_json['user']['media']['nodes'][i]['likes'])

# 判断是否已入库
def is_in(code):
	conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
									 port="5432")
	if conn:
		cur = conn.cursor()

		cur.execute("SELECT star_id, code from star_img WHERE code = '" + code + "' AND star_id = '"+ star_id+"'")

		rows = cur.fetchall()
		if len(rows) > 0:
			print(rows[0][0], rows[0][1])
			conn.commit()
			conn.close()
			sys.exit()

# 获取单条内容的详细信息
def get_p_info(_code,_like):
	# if current_page<16:
	# 	print('current_page'+str(current_page))
	# 	return  False
	# 判断是否已经入库
	is_in(_code)
	# 更新请求头
	_ua = UserAgent()
	headers['Referer'] = ins_url + '/p/' + _code
	headers['Accept'] = '*/*'
	headers['Content-Length'] = '0'
	headers['Host'] = 'www.insstar.cn'
	headers['Origin'] = ins_url
	headers['X-Requested-With'] = 'XMLHttpRequest'
	headers['User-Agent'] = _ua.random
	__url = ins_url+'/p/'+_code
	time.sleep(1)
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
	# 获得此条 ins 的详细信息，解析处理后待入库
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
	origin_url = 'https://insstar.cn/p/'+_code
	print('Instagram',display_url,take_at_timestamp,attitudes_count,is_video,video_url)
	# print(pic_detail)
	if _json['sidecar'] and len(_json['sidecar'])>0:
		for i in range(2,len(_json['sidecar'])):
			pic_detail = None
			display_url = _json['sidecar'][i]['display_url']
			print(pic_detail,display_url)
			conn2 = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
									 port="5432")
			if conn2:
				cur1 = conn2.cursor()
				cur1.execute("INSERT INTO star_img (star_id,origin,attitudes_count,text,code,display_url,pic_detail,take_at_timestamp,is_video,video_url,status,created_at,updated_at,origin_url) \
				                                                                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
							 (star_id, 'instagram', attitudes_count, text[0:255],
							  _code, display_url, json.dumps(pic_detail), take_at_timestamp, is_video, video_url,
							  status, created_at, updated_at,
							  origin_url))
				conn2.commit()
			else:
				conn2.close()
	conn1 = psycopg2.connect(database=db_name, user=db_user, password=db_password, host="127.0.0.1",
								 port="5432")
	if conn1:
		cur1 = conn1.cursor()
		cur1.execute("INSERT INTO star_img (star_id,origin,attitudes_count,text,code,display_url,pic_detail,take_at_timestamp,is_video,video_url,status,created_at,updated_at,origin_url) \
		                                                                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
						 (star_id, 'instagram', attitudes_count, text[0:255],
						  _code, display_url, json.dumps(pic_detail), take_at_timestamp,is_video, video_url,status, created_at, updated_at,
						  origin_url))
		conn1.commit()
	else:
		conn1.close()

# 第一页内容
get_first_page_data(soup)
# 第二页内容
get_second_page_data(next_cursor, rg, has_next_page, _uid)


#从第三页以及剩余的内容
for i in range(1, int(math.ceil(total / 12)-1)):
	print('current_page: '+str(i+2))
	# global current_page
	# current_page = i+2
	# print(i)
	time.sleep(1)
	if i % 7 == 0:
		print('---休眠20秒--')
		time.sleep(20)
	if has_next_page:
		# 获取下一页的 ins 内容
		get_next_data(next_cursor, rg, has_next_page, _uid)


