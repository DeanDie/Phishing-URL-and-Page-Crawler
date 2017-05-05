#!/usr/bin/env python
#-*- coding:utf-8 -*-

import dbHelper
import codecs
from PIL import Image

report_date = "20170428.log"

with open('../logs/' + report_date, 'r') as f:

	for line in f.readlines():
		urlData = line.strip().split()
		urlData[0] = urlData[0].decode('utf-8')
		urlData[1] = urlData[1].decode('utf-8')
		print(urlData[0])
		threat_info = dbHelper.fetch(urlData[1])
		if threat_info  != None:
			file = codecs.open('./data/inTable/1.txt', 'a', encoding='utf-8')
			if threat_info[0] is not None:
				file.writelines(urlData[0] +'\t' + urlData[1] + '\t' + threat_info[0] + '\r\n')
			else:
				file.writelines(urlData[0] + '\t' + urlData[1] + '\r\n')
			file.close()
		else:
			file = codecs.open('./data/outOfTable/2.txt', 'a',  encoding='utf-8')
			file.writelines(urlData[0]+ '\t' + urlData[1] + '\r\n')
			print "###########################################/n#################################"
			file.close()


	f.close()