
import requests
import time
import os
import postfile
import json as simplejson
import urllib
import urllib2
import csv

file_dir = '/home/spark/prog/dealpkg/down/'

class Compare():
	def __init__(self):
		self.paramters = {'apikey': 'ed7cdfff8ea245049a00f8b7c8ffa38775f8a79034204e9cb814d0a1acb92f79'}
		self.softList = os.listdir(file_dir)
		self.failedSoft = []
		self.resource = {}

	def store(self, row):
		headers = ['Name', 'ans']
		if os.path.isfile('ans.csv'):
			os.remove('ans.csv')
		with open('ans.csv', 'a') as file:
			f_csv = csv.DictWriter(file, headers)
			f_csv.writerow()
			file.close()

	def uploads(self):

		for soft_name in self.softList:
			size = os.path.getsize(soft_name)
			if size >= 80 * 1024:
				self.failedSoft.append(soft_name)
				continue
			host = "x.threatbook.cn"
			selector = "https://x.threatbook.cn/api/v1/file/scan"
			fields = [("apikey", self.paramters['apikey'])]
			file_content = open(file_dir + soft_name, 'rb').read()
			files = [("file", "sample.txt", file_content)]
			json = postfile.post_multipart(host, selector, fields, files)
			self.resource[soft_name] = json["resource"]
			# TODO

	def getReport(self):
		for soft_name in self.softList:
			url = 'https://x.threatbook.cn/api/v1/file/report'
			params = self.paramters
			params['resource'] = self.resource[soft_name]
			data = urllib.urlencode(params)
			req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
			json_data = response.read()
			json_data = simplejson.loads(json_data)
			report = json_data['scan']

			soft_name_ans = True
			for key, value in report:
				if value['detected'] == False:
					soft_name_ans = False
					break
			self.store((soft_name, soft_name_ans))


if __name__ == '__main__':
	compare = Compare()

