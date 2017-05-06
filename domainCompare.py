#!/usr/bin/env python
#-*- coding:utf-8 -*-

import dbHelper
# import codecs
import time
import re
import os
import csv

date = time.strftime('%Y%m%d', time.localtime())
report_date = date + ".log"

pattern = re.compile(r'^http(.*gpic.*|www\.eversec\.com\.cn|.*sina.*|.*sohu.*|.*weibo.*|.*youku.*|.*baidu.*|.*taobao.*|.*qq.*)$', re.I)


files = ['ln', 'sx']

attributes = ('url', 'domain', 'degree', 'detect_date', 'type', 'report_date', 'report_hour', 'app_web_threat_info')

if os.path.isfile('./data/count.txt'):
	os.remove('./data/count.txt')
count_file = open('./data/count.txt', 'a')

for fileName in files:

	count = 0
	with open('../logs/' + fileName + '/' + report_date, 'r') as f:
		with open('./data/' + fileName + '/' + date + '.csv', 'w') as file:
			f_csv = csv.writer(file)
			f_csv.writerow(attributes)
			file.close()
		with open('./data/' + fileName + '/' + date + '_Undo.csv', 'w') as file:
			f_csv = csv.writer(file)
			f_csv.writerow(attributes)
			file.close()

		for line in f.readlines():
			urlData = line.strip().split()
			if re.search(pattern, urlData[0]):
				count += 1
				continue

			print urlData
			print(urlData[0])
			threat_info = dbHelper.fetch(urlData[1])
			if threat_info  != None:
				if threat_info[0] != None:
					threat_info = threat_info[0].encode('utf-8')
					urlData.append(threat_info)
				with open('./data/' + fileName + '/' + date + '.csv', 'a') as file:
					f_csv = csv.writer(file)
					f_csv.writerow(urlData)
					file.close()
			else:
				with open('./data/' + fileName + '/' + date + '_Undo.csv', 'a') as file:
					f_csv = csv.writer(file)
					f_csv.writerow(urlData)
					file.close()

		f.close()
	count_file.write(str(count) + '\r\n')