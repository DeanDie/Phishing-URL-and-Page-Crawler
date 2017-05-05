#coding:utf-8
import requests
from bs4 import BeautifulSoup
import chardet
import urllib2

url = "http://007swz.com"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebK Gecko) Chrome/54.0.2840.98 Safari/537.36'
	}

# r = urllib2.urlopen(url, timeout=10).read()
#
# encoding_dict = chardet.detect(r)
#
# web_encoding = encoding_dict['encoding']
# if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
#
# 	html = r
# else:
# 	html = r.decode('gbk', 'ignore').encode('utf-8')
html = requests.get(url, headers).content

str_type = chardet.detect(html)
code = str_type['encoding']
print code
if code == 'utf-8' or code == 'UTF-8':

	html = html
else:
	html = html.decode('gbk', 'ignore').encode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

title = ""

# print r.encoding

title = soup.title if (soup.title) else ""
print title

content = soup.body.text
print content

print title
title = title.decode('utf8')

print title