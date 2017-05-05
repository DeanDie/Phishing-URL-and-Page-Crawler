# coding=utf-8

import requests
import json
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor
import re
from phishingDao import urlDB


headers = {"User-Agent": "Mozilla/6.0 (Windows NT 7.1 WOW64) AppleWebKit/"}

lock = threading.Lock()

domain = 'http://www.phishtank.com/'

pattern = re.compile(r'<div>\s*<b>(.*?)\s*</b>', re.S | re.M | re.I)

def eachPage(i):
	url = domain + "phish_search.php?page=%s&valid=y&Search=Search" % str(i)

	urlList, links = [], []
	visted = set()

	try:
		eachHeaders = {}
		eachHeaders["User-Agent"] = headers["User-Agent"] + str(i)
		content = requests.get(url, headers=eachHeaders)
		soup = BeautifulSoup(content.text, 'lxml')

		table = soup.find_all('tr')
		for oneRow in table[1: len(table) - 1]:
			# print oneRow.find_all('td')[1].get_text().split('add',1)[0]
			link = oneRow.find('td').a.get('href')
			if link != None:
				links.append(domain + link)

	except Exception as e:
		print e

	finally:
		if links:
			for link in links:
				eachHeaders["User-Agent"] = str(links.index(link)) + headers["User-Agent"]
				text = requests.get(link, headers=eachHeaders).text
				blackUrl = re.search(pattern, text).group(1)
				if blackUrl not in visted and len(blackUrl) < 1000:
					urlList.append(blackUrl)
					visted.add(blackUrl)
					print blackUrl
			if urlList != []:
				lock.acquire()
				urlDB.insertBlacklist(urlList)
				lock.release()

if __name__ == '__main__':
	pool = ThreadPoolExecutor(max_workers=100)
	for i in range(1, 3300):
		pool.submit(eachPage, (i))

