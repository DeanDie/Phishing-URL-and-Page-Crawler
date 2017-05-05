#!/usr/bin/env python
# coding=utf-8

import requests
from phishingDao import urlDB
import re
import threading
from concurrent.futures import ThreadPoolExecutor


lock = threading.Lock()
lockSet = threading.Lock()

pattern = re.compile(r'href="(.*?)"', re.I | re.M | re.S)
pre_suffixPattern = re.compile(r"^http.*?(?<!css|\.js|ico|png|gif|jpg|png|xml)$", re.I)

jsonData = []
for pageId in range(1, 4):
	requestUrl = "http://index.iresearch.com.cn/pc/GetDataList/?classId=0&timeId=49&orderBy=2&pageIndex=" + str(pageId) +"&pageSize=1000"
	headers = {
				"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36",
				"Host": "index.iresearch.com.cn",
				"Referer": "http://index.iresearch.com.cn/Pc/List"
		   }
	try:
		json = requests.get(requestUrl, headers=headers).json()["List"]
		if json != None:
			jsonData.extend(json)
	except Exception as e:
		print e

headers = {}
visited = set()

def eachDomain(singerUrl):
	table = []
	domain = singerUrl["Domain"]
	siteName = singerUrl["AppName"]
	className = singerUrl["KclassName"]
	table.append([domain, siteName, className])
	# urlDB.insert('whitelist', table)

	headersDomain = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/"}
	try:
		text = requests.get("http://www." + domain, headers=headersDomain).text
	except :
		try:
			text = requests.get("http://www." + domain, headers=headersDomain).text
		except Exception as e:
			print e
			return

	url, newUrl = [], []
	url = re.findall(pattern, text)
	for i in range((len(url))):
		lockSet.acquire()
		if re.match(pre_suffixPattern, url[i]) and url[i] not in visited:
			visited.add(url[i])
			newUrl.append(url[i])
		lockSet.release()
	url = newUrl

	if len(url) >= 20:
		url = url[:20]
	else:
		for eachUrl in url:
			try:
				headers["User-Agent"] = headersDomain["User-Agent"] + str(url.index(eachUrl))
				text = requests.get(eachUrl, headers=headers).text
				for subUrl in re.findall(pattern, text):
					lockSet.acquire()
					if re.match(pre_suffixPattern, subUrl) and subUrl not in visited:
						visited.add(subUrl)
						url.append(subUrl)
					lockSet.release()
					if len(url) >= 20:
						url = url[:20]
						break
			except Exception as e:
				print e
	if len(url) > 0:
		lock.acquire()
		print domain, len(url)
		urlDB.insert(url)
		lock.release()

# for singerUrl in jsonData:
# 	thread = threading.Thread(target=eachDomain, args=(singerUrl,))
# 	thread.start()

data = []

for singerUrl in jsonData:
	data.append("http://" + singerUrl["Domain"])
urlDB.insert(data)

pool = ThreadPoolExecutor(max_workers=200)
for singerUrl in jsonData:
	pool.submit(eachDomain, (singerUrl))

print "Completed!"

