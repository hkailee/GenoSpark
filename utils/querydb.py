#!/usr/local/bin/python3

"""
run a query string, display formatted result table
example: querydb.py dbase1 "select name, job from people where pay > 50000"
"""

import sys
from loaddb import login
from makedictsFromSQL import makedicts
from dumpdb import showformat

if input('Are you sure?').lower() not in ('y', 'yes'):
    sys.exit()

database, querystr = 'dbase_Sqlite', 'select * from people'
if len(sys.argv) > 1: database = sys.argv[1]
if len(sys.argv) > 2: querystr = sys.argv[2]
conn, curs = login(database)
rows = makedicts(curs, querystr)
showformat(rows)