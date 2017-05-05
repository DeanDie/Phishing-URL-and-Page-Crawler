# -*- coding: utf-8 -*-
from phishingDao import urlDB
import requests
import regex
import re
import multiprocessing
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import threading

urlTable = list(urlDB.fetchAll("whitelist"))

suffixPattern = re.compile(r"^(http|ftp|https).*\.(zip|rar|exe|apk|sis|sisx|jar|cab)$", re.I)

headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'Cookie': 'CUPID=607763183609f4605b630ef6448180a2',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
	}

# lock = threading.Lock()
def work(url):

	validUrl = re.compile(r'^(http|ftp)s?:/{2}\w.+$', re.I)

	if (not re.match(validUrl, url)) or re.match(suffixPattern, url):
			urlDB.deleteOne('whitelist', url)
			print url, "Deleted!"
	else:
		print url, "Valid"


# pool = ThreadPoolExecutor(max_workers=500)
# for url in urlTable:
# 	url = url[0]
# 	pool.submit(work, url)
#
# pool.shutdown(wait=True)
#
# print 'test'
# if len(toDelete) > 0:
# 	urlDB.delete(toDelete)

"""
去除末尾的'/'
"""
def delSlash(tableName):
	url = urlDB.fetchAll(tableName)
	print url[0][0]
	url = [eachUrl[0] for eachUrl in url]
	for eachUrl in url:
		if eachUrl[-1] == '/':
			tmp = eachUrl[:-1]
			if tmp not in url:
				urlDB.insertOne(tableName, tmp)
			urlDB.deleteOne(tableName, eachUrl)
			print "OK"

'''
过滤下载文件URL
'''
def delInvalidSuffix(tableName):
	url = urlDB.fetchAll(tableName)
	url = [eachUrl[0] for eachUrl in url]
	for eachUrl in url:
		print eachUrl
		if re.match(suffixPattern, eachUrl):
			urlDB.deleteOne(tableName, eachUrl)
			print 'Deleted!'

# delInvalidSuffix('whitelist')