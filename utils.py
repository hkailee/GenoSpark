#!/usr/local/bin/python3

import sqlite3

##############################################
### Login to database
##############################################

def login(dbfile):
    conn = sqlite3.connect(dbfile)  # create or open db file
    curs = conn.cursor()
    return conn, curs

##############################################
### Create new database
##############################################

def makedb(dbfile, table, columnFeatures):
    columnFeatures = input("eg: (Column1 char(30), Column2 char(10), Column3 int(4))")
    conn, curs = login(dbfile)
    command = 'create table %s %s' % table % columnFeatures
    curs.execute(command)
    conn.commit()

##############################################
### Load Data
##############################################

def loaddb(curs, table, datafile, conn=None, verbose=True):
    file = open(datafile)                               # x,x,x\nx,x,x\n
    rows = [line.rstrip().split(',') for line in file]  # [[x,x,x], [x,x,x]]
    rows = [str(tuple(rec)) for rec in rows]            # ["(x,x,x)", "(x,x,x)"]
    for recstr in rows:
        curs.execute('insert into ' + table + ' values ' + recstr)
    if conn:
        conn.commit()
    if verbose:
        print(len(rows), 'rows loaded')

##############################################
### Make dictionaries from SQL
##############################################
def makedicts(cursor, query, params=()):
    cursor.execute(query, params)
    colnames = [desc[0] for desc in cursor.description]
    rowdicts = [dict(zip(colnames, row)) for row in cursor.fetchall()]
    return rowdicts

##############################################
### Dump Data from Dictionaries
##############################################

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

##############################################
### Remove a table from Database
##############################################

def cleardb(cursor, table):
    cursor.execute('delete from ' + table)
