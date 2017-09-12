#!/usr/local/bin/python3


"""
delete all rows in table, but don't drop the table or database it is in usage: cleardb.py dbname? tablename?
"""

import sys
from loaddb import login

if input('Are you sure?').lower() not in ('y', 'yes'):
    sys.exit()

dbname = (len(sys.argv) > 1 and sys.argv[1]) or 'dbase_Sqlite'
table = (len(sys.argv) > 2 and sys.argv[2]) or 'people'

conn, curs = login(dbname)
curs.execute('delete from ' + table)
print(curs.rowcount, 'records deleted') # conn closed by its __del__
conn.commit()                           # else rows not really deleted