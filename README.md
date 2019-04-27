# 图片爬虫

## 保存数据到数据库

* `wb.py` 微博图片爬虫(可能会 cookie 过期)

* `ins.py` ins 图片爬虫 (来源网站服务器不稳定


> downloadImageToLocal

## `downloadWeiboImage` 

- `downloadWeiboImage.py`  下载微博图片到本地

## 技术说明

> python 版本： 3.7

> 数据库： PostgreSQL

## sql

该目录下，是该项目数据库需要的表结构。具体名字和文件内容一一对应。

`star.sql` 是其他三个文件的依赖文件。提供一个 unique key(其他文件中的 star_id 即该表中的 id)

## 注意

新浪微博如果你短时间内请求太多，肯能会被封 ip ...