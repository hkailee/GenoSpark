#!/usr/local/bin/python3

"""
display table contents as raw tuples, or formatted with field names command-line usage:
dumpdb.py dbname? table? [-] (dash=formatted display)
"""

import sys
from loaddb import login
from makedictsFromSQL import makedicts

def showformat(recs, sept=('-' * 40)):
    print(len(recs), 'records')
    print(sept)
    for rec in recs:
        maxkey = max(len(key) for key in rec)               # max key len
        for key in rec:                                     # or: \t align
            print('%-*s => %s' % (maxkey, key, rec[key]))   # -ljust, *len
        print(sept)

def dumpdb(cursor, table, format=True):
    if not format:
        cursor.execute('select * from ' + table)
        while True:
            rec = cursor.fetchone()
            if not rec:
                break
            print(rec)
    else:
        recs = makedicts(cursor, 'select * from ' + table)
        showformat(recs)

if __name__ == '__main__':
    dbname, format, table = 'dbase_Sqlite', False, 'people'
    cmdargs = sys.argv[1:]
    if '-' in cmdargs:
        format = True
        cmdargs.remove('-')
    if cmdargs:
        dbname = cmdargs.pop(0)
    if cmdargs:
        table = cmdargs[0]

    conn, curs = login(dbname)
    dumpdb(curs, table, format)