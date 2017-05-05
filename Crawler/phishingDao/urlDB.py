# -*- coding:utf-8 -*-
import pymysql


"""
黑白名单表操作
"""


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

def insert(infolist):
	conn = connect()

	for row in infolist:
		try:
			cur = conn.cursor()
			sql = 'insert into whitelist VALUES(%s);'
			cur.execute(sql, row)
			conn.commit()
			print "Success!"
		except Exception as e:
			print e
		finally:
			if cur:
				cur.close()

	if conn:
		conn.close()


def insertBlacklist(infolist):
	try:
		conn = connect()
		cur = conn.cursor()
		sql = 'insert into blacklist VALUES(%s);'
		cur.executemany(sql, infolist)
		conn.commit()
	except Exception as e:
		print e
	finally:
		if cur:
			cur.close()
		if conn:
			conn.close()

def fetchAll(tableName):
	results = []
	try:
		conn = connect()
		cur = conn.cursor()
		sql = 'select url from %s;' % tableName
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

def delete(rows):
	try:
		conn = connect()
		cur = conn.cursor()
		sql = "DELETE FROM whitelist WHERE url = %s;"
		cur.executemany(sql, rows)
		conn.commit()
	except Exception as e:
		print e
	finally:
		if cur:
			cur.close()
		if conn:
			conn.close()

def insertOne(tableName, info):
	try:
		conn = connect()
		cur = conn.cursor()
		sql = 'insert into ' + tableName + ' VALUES(%s);'
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
