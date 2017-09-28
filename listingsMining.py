#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys

db_host = 'postgreinstance1.cmqiuzqh62x2.us-east-1.rds.amazonaws.com'
db_port = 5432
db_name = "dbpostgre1"
db_user = "postgremaster1"
db_pass = "postgremaster1"
db_table = "Products"

con = None

try:
    con = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name, db_user, db_host, db_pass))
    cur = con.cursor()
    cur.execute("SELECT * FROM %s" % db_table)
    while True:
        row = cur.fetchone()
        if row == None:
            break
        print("Product: " + row[1] + "\t\tPrice: " + str(row[2]))
except psycopg2.DatabaseError as e:
    if con:
        con.rollback()
    print('Error %s' % e)
    sys.exit(1)

finally:
    if con:
        con.close()