#!/usr/local/bin/python3

"""
physically delete and re-create database files usage: makedb.py dbname? tablename?
"""

import sys
from loaddb import login

if input('Are you sure?').lower() not in ('y', 'yes'):
    sys.exit()

dbname = (len(sys.argv) > 1 and sys.argv[1]) or 'dbase_Sqlite'
table = (len(sys.argv) > 2 and sys.argv[2]) or 'people'

conn, curs = login(dbname)
try:
    curs.execute('drop table ' + table)
except:
    print('database table did not exist')

command = 'create table %s (name char(30), job char(10), pay int(4))' % table
curs.execute(command)
conn.commit()               # commit may be optional here
print('made', dbname, table)