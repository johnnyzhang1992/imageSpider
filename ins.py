# !/usr/bin/python
# encoding:utf-8
# 这个例子是去获取ins里的图片，因为墙，所以爬的是一个国内的站

from selenium import webdriver
import time
import math
import requests
import urllib.request
import json
from bs4 import BeautifulSoup
import os
import sys

request_params = {"ajwvr":"6","domain":"100505","domain_op":"100505","feed_type":"0","is_all":"1","is_tag":"0","is_search":"0"}
profile_request_params = {"profile_ftype":"1","is_all":"1"}

ins_url = "http://www.insstar.cn"

# 林允儿
user_id = 'yoona__lim'
# user_id = input('请输入所要爬取的用户username:')

_url = ins_url+'/'+str(user_id)

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

req = requests.get(_url, headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')

_uid = soup.find(id='username')
_uid = _uid.attrs['data-uid']
print('uid: '+_uid)
_list = soup.find(id='list')
next_cursor = _list.attrs['next-cursor']
rg = _list.attrs['data-rg']
print('cursor: '+next_cursor)
print('rg: '+rg)
total = 0

# 数据获取方式
# 第一步，获取 p 元素的 code
# 第二部，根据 code 获取图片或者视频的详细信息

# 用户第一页内容
def get_first_page_data(_soup):
	items = _soup.find_all('div',class_='img-wrap')
	if int(len(items)) > 0:
		print('items-length:'+str(len(items)))
		for i in range(0,int(len(items))):
			print(items[i].attrs['data-code'])
			# get_p_info(items[i].attrs['data-code'])


# 获取下一页内容
def get_more_data(_next_cursor, _rg, _has_next_page, __uid):
	print(_next_cursor,_rg,_has_next_page,__uid)
	if _next_cursor != '' and _rg != '' and _has_next_page:
		__url = ' http://www.insstar.cn/user/yoona__lim?next='+_next_cursor+'&uid='+__uid+'&rg='+_rg
		print(__url)
		headers['Referer'] = ins_url+'/'+user_id
		headers['Accept'] = '*/*'
		headers['Content-Length'] = '0'
		headers['Host'] =  'www.insstar.cn'
		headers['Origin'] =ins_url
		headers['X-Requested-With'] = 'XMLHttpRequest'
		# print(headers)
		response = requests.post(__url, headers=headers)
		_json = json.loads(response.text)
		# print(_json)
		global next_cursor
		global has_next_page
		next_cursor= _json['user']['media']['page_info']['end_cursor']
		has_next_page= _json['user']['media']['page_info']['has_next_page']
		print(next_cursor,has_next_page)
		if len(_json['user']['media']['nodes'])>0:
			for i in range(0,int(len(_json['user']['media']['nodes']))):
				# code
				print(_json['user']['media']['nodes'][i]['code'])
				# 获取当前页面的所有单条内容的详细信息
				# get_p_info(_json['user']['media']['nodes'][i]['code'])


def get_second_page_data(_next_cursor, _rg, _has_next_page, __uid):
	print(_next_cursor, _rg, _has_next_page, __uid)
	if _next_cursor != '' and _rg != '' and _has_next_page:
		__url = ' http://www.insstar.cn/user/yoona__lim?next=' + _next_cursor + '&uid=' + __uid + '&rg=' + _rg
		print(__url)
		headers['Referer'] = ins_url + '/' + user_id
		headers['Accept'] = '*/*'
		headers['Content-Length'] = '0'
		headers['Host'] = 'www.insstar.cn'
		headers['Origin'] = ins_url
		headers['X-Requested-With'] = 'XMLHttpRequest'
		# print(headers)
		response = requests.post(__url, headers=headers)
		_json = json.loads(response.text)
		global total
		global next_cursor
		global has_next_page
		total= _json['user']['media']['count']
		next_cursor= _json['user']['media']['page_info']['end_cursor']
		has_next_page= _json['user']['media']['page_info']['has_next_page']
		print('total:'+str(total))
		print('total_page:'+str(math.ceil(total / 12)))
		if len(_json['user']['media']['nodes'])>0:
			for i in range(0,int(len(_json['user']['media']['nodes']))):
				# code
				print(_json['user']['media']['nodes'][i]['code'])
				# 获取当前页面的所有单条内容的详细信息
				# get_p_info(_json['user']['media']['nodes'][i]['code'])



# 获取单条内容的详细信息
def get_p_info(_code):
	headers['Referer'] = ins_url + '/p/' + _code
	headers['Accept'] = '*/*'
	headers['Content-Length'] = '0'
	headers['Host'] = 'www.insstar.cn'
	headers['Origin'] = 'http://www.insstar.cn'
	headers['X-Requested-With'] = 'XMLHttpRequest'
	__url = ins_url+'/p/'+_code
	response = requests.post(__url, headers=headers)
	# 详细信息，待处理入库
	_json = json.loads(response.text)
	print(_json)

# 第一页内容
# get_first_page_data(soup)
get_second_page_data(next_cursor, rg, has_next_page, _uid)

for i in range(1, int(math.ceil(total / 12))):
	print('current_page'+str(i+2))
	time.sleep(1)
	if has_next_page:
		get_more_data(next_cursor, rg, has_next_page, _uid)


