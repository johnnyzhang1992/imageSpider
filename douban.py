#coding=utf-8

import urllib
# import urllib2
import re
from bs4 import BeautifulSoup

y=1
#设置下载页数，进行循环，当前为3页
for y in range(1,4):
    page=(y-1)*40
    url="http://movie.douban.com/celebrity/1018980/photos/?type=C&start=%s&sortby=vote&size=a&subtype=a" %page
    content=urllib.urlopen(url).read()

    soup=BeautifulSoup(content)
    img_all=soup.find_all("img",src=re.compile('.douban.com/view/photo'))
    #下载链接头中有img3,img5，故正则时不写进去

    print("正下载第%s页" %y)
    x=40*y
    for img in img_all:
        img_str=img["src"]
        img_b=img_str.replace("thumb","photo")
        img_name="%s-%s.jpg" %(y,x)
        path="D:\\Python_data\\gyy\\"+img_name    #保存图片路径
        urllib.urlretrieve(img_b,path)
        x += 1
    y += 1

print("已下载%s张图片" %x*y)
