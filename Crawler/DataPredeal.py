# -*- coding: utf-8 -*-
import dbHelper
import requests
import regex
import re
import multiprocessing
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import threading

urlTable = list(dbHelper.fetchAll("whitelist"))

suffixPattern = re.compile(r"^http.*(?<=\.zip|\.rar|\.exe|\.apk|\.sis|sisx|\.jar|\.cab)$", re.I)

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

lock = threading.Lock()
def work(url):
	if url[-1] == r'/':
		url = url[:-1]

	try:
		data = requests.get(url, headers=headers, timeout=10)
		print url, "Normal"
	except Exception as e:
		e = str(e.message)
		# print str(e.message)
		if (len(e) >= 15 and e[:15] == "Failed to parse") or (len(e) >= 11 and e[:11] == "Invalid URL"):

			dbHelper.deleteOne('whitelist', url)


pool = ThreadPoolExecutor(max_workers=500)
for url in urlTable:
	url = url[0]
	pool.submit(work, url)
#
# pool.shutdown(wait=True)
#
# print 'test'
# if len(toDelete) > 0:
# 	dbHelper.delete(toDelete)

"""
去除末尾的'/'
"""
def delSlash(tableName):
	url = dbHelper.fetchAll(tableName)
	print url[0][0]
	url = [eachUrl[0] for eachUrl in url]
	for eachUrl in url:
		if eachUrl[-1] == '/':
			tmp = eachUrl[:-1]
			if tmp not in url:
				dbHelper.insertOne(tableName, tmp)
			dbHelper.deleteOne(tableName, eachUrl)
			print "OK"

'''
过滤下载文件URL
'''
def delInvalidSuffix(tableName):
	url = dbHelper.fetchAll(tableName)
	url = [eachUrl[0] for eachUrl in url]
	for eachUrl in url:
		print eachUrl
		if re.match(suffixPattern, eachUrl):
			dbHelper.deleteOne(tableName, eachUrl)
			print 'Deleted!'

# delInvalidSuffix('whitelist')