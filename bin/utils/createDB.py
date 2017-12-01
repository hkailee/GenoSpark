#!/usr/local/bin/python3

import sqlite3, ast

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
    #columnFeatures = input("eg: (Column1 char(30), Column2 char(10), Column3 int(4))")
    conn, curs = login(dbfile)
    try:
        curs.execute('drop table ' + table)
        print('Dropped table ' + table)
    except:
        print('database table did not exist')
    command = 'create table %s %s' % (table, columnFeatures)
    curs.execute(command)
    conn.commit()

##############################################
### Load Data
##############################################

def loaddb(table, dbfile, datafile, conn=None, verbose=True):
    conn, curs = login(dbfile)
    file = open(datafile)
    rows = [line.rstrip().split('\t') for line in file]  # [[x,x,x], [x,x,x]]
    rows = [str(tuple(rec)) for rec in rows[1:]]            # ["(x,x,x)", "(x,x,x)"]
    for recstr in rows:
        curs.execute('insert into ' + table + ' values ' + recstr)
    if conn:
        conn.commit()
    if verbose:
        print(len(rows), 'rows loaded')
        
def loaddb_chineseData(table, dbfile, datafile, conn=None, verbose=True):
    conn, curs = login(dbfile)
    file = open(datafile)
    rows = [line.rstrip().split('\t') for line in file]  # [[x,x,x], [x,x,x]]
    rows = [str(tuple(rec)) for rec in rows[1:]]            # ["(x,x,x)", "(x,x,x)"]
    for recstr in rows:
        if len(ast.literal_eval(recstr)) == 6:
            #print(len(ast.literal_eval(recstr))
            curs.execute('insert into ' + table + '(CHROM, POS, N_ALLELES, N_CHR, Chinese_ALLELE_FREQ_1, Chinese_ALLELE_FREQ_2)' + ' values ' + recstr)
        if len(ast.literal_eval(recstr)) == 7:
            curs.execute('insert into ' + table + '(CHROM, POS, N_ALLELES, N_CHR, Chinese_ALLELE_FREQ_1, Chinese_ALLELE_FREQ_2, Chinese_ALLELE_FREQ_3)' + ' values ' + recstr)
        if len(ast.literal_eval(recstr)) == 8:
            curs.execute('insert into ' + table + '(CHROM, POS, N_ALLELES, N_CHR, Chinese_ALLELE_FREQ_1, Chinese_ALLELE_FREQ_2, Chinese_ALLELE_FREQ_3, Chinese_ALLELE_FREQ_4)' + ' values ' + recstr)
    if conn:
        conn.commit()
    if verbose:
        print(len(rows), 'rows loaded')
        
##############################################
### Combining tables
##############################################

def combinetables(dbfile, table, query):
    #columnFeatures = input("eg: (Column1 char(30), Column2 char(10), Column3 int(4))")
    conn, curs = login(dbfile)
    try:
        curs.execute('drop table ' + table)
        print('Dropped table ' + table)
    except:
        print('database table did not exist')
    command = 'create table %s as %s' % (table, query)
    curs.execute(command)
    conn.commit()

###################################################################################################
### Load Data manually from a raw vcf -
### Mainly created for the Singapore Malay vcf as
### command: bcftools query -f '%CHROM\t%POS\t%ID\n' SSM.chr8.2012_05.genotypes.vcf.gz -o chr8_rsID
### produced error as such: [E::bcf_hdr_add_sample] Empty sample name: trailing spaces/tabs in 
### the header line?
###################################################################################################

def loaddb_vcf_rsID(table, dbfile, datafile, conn=None, verbose=True):
    conn, curs = login(dbfile)
    file = open(datafile)
    rows = [line.rstrip().split('\t') for line in file]  # [[x,x,x], [x,x,x]]
    rows = [str(tuple(rec[:3])) for rec in rows[11:]]            # ["(x,x,x)", "(x,x,x)"]
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

def dumpdb(dbfile, table, num=10, format=False):
    conn, curs = login(dbfile)
    if not format:
        curs.execute('select * from ' + table)
        while True:
            rec = curs.fetchmany(num)
            if not rec:
                break
            for row in rec:
                print(row)
    else:
        recs = makedicts(curs, 'select * from ' + table)
        showformat(recs)

##############################################
### Remove a table from Database
##############################################

def cleardb(dbfile, table):
    conn, curs = login(dbfile)
    try:
        curs.execute('DROP TABLE ' + table)
    except:
        pass
    conn.commit()
