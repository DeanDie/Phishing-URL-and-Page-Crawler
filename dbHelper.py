# -*- coding:utf-8 -*-
import pymysql

def connect():
    conn = pymysql.connect(
        host='10.1.1.181',
        user='root',
        passwd='secsmarts',
        db='cyd',
        charset='utf8'
    )
    return conn

def fetch(urlDomain):
	results = []
	try:
		conn = connect()
		cur = conn.cursor()
		sql = 'select threat_info from  app_web_threat_info where DOMAIN = %s;'
		cur.execute(sql, urlDomain)
		results = cur.fetchone()

	except Exception as e:
		print(e)

	finally:
		if cur:
			cur.close()
		if conn:
			conn.close()
		return results
