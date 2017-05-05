# -*- coding:utf-8 -*-
import pymysql

def connect():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='yongheng',
        db='webspyder',
        charset='utf8'
    )
    return conn

def connectRemote():
	conn = pymysql.connect(
		host='10.1.1.181',
		user='mokun',
		passwd='secsmarts',
		db='webspyder',
		charset='utf8'
	)

def fetchAll(tableName):
	results = []
	try:
		conn = connect()
		cur = conn.cursor()
		sql = 'select url from pagefeatrue;'
		cur.execute(sql)
		results = cur.fetchall()

	except Exception as e:
		print e

	finally:
		if cur:
			cur.close()
		if conn:
			conn.close()
		return results

def insertOne(info):
	try:
		conn = connect()
		cur = conn.cursor()
		sql = 'insert into pagefeatrue VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);'
		cur.execute(sql, info)
		conn.commit()
	except Exception as e:
		print e
	finally:
		if cur:
			cur.close()
		if conn:
			conn.close()


def deleteOne(tableName, info):
	try:
		conn = connect()
		cur = conn.cursor()
		sql = 'delete from ' + tableName +' WHERE url = (%s);'
		cur.execute(sql, info)
		conn.commit()
	except Exception as e:
		print e
	finally:
		if cur:
			cur.close()
		if conn:
			conn.close()