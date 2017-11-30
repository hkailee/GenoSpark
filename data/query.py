#!/usr/bin/env python3

import datetime, os, subprocess, sys, time
import pandas as pd
import multiprocessing
import threading
from threading import BoundedSemaphore
# from utils import logDecorator as lD

sys.path.append(os.path.abspath('..'))

if __name__ == '__main__':
    from bin.utils.createDB import *

    ################
    ### Creating sql table for the input
    ################

    xls_file = pd.ExcelFile('query.xlsx')
    table = xls_file.parse('Sheet1')
    # chrom = [x for x in table['Chr'].unique()[:-1]]
    conn = sqlite3.connect('../dbase_Sqlite')
    try:
        cleardb('../dbase_Sqlite', 'dataFrame')
        print('Drop dataFrame')
    except:
        pass
    table.to_sql('dataFrame', conn)

    ################
    ### Querying from Chinese, Malay and Indian populations
    ################

    startTime = time.time()

    query = """
            SELECT DISTINCT
                dataFrame.*, CMI.*
            FROM
                dataFrame LEFT OUTER JOIN 
                CMI ON dataFrame.Coordinate=CMI.POS 
                AND dataFrame.Chr=CMI.CHROM
            """
    df = pd.read_sql_query(query, conn)

    timeTaken = time.time()-startTime
    print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
          '- Data Retrieval for all races completed: Took {} seconds to complete.'.format(timeTaken))

    df_working = df[:]

    for ethnic in ['Indian', 'Malay', 'Chinese']:
        df_Null_temp = df_working[df_working[ethnic + "_ALLELE_FREQ_1"].isnull()]
        for chrom in list(range(1, 23)) + ['X']:
            df_Null_temp_working = df_Null_temp[(df_Null_temp.Chr.astype(str) == str(chrom))]
            with open('query.bed', 'w') as bedFile:
                for i in df_Null_temp_working['Coordinate']:
                    bedFile.write('chr' + str(chrom) + '\t' + str(i - 1) + '\t' + str(i) + '\n')
            with open('output.fa', 'w') as outfile:
                proc = subprocess.Popen(['seqtk', 'subseq', 'data/GRCh37/chr' + str(chrom) + '.fa', 'query.bed'],
                                        stdin=subprocess.PIPE, stdout=outfile)
                out, err = proc.communicate()

            p = open('output.fa', "r")
            for i in df_Null_temp_working.index:
                p.readline()
                df_working.loc[(df_working.index == i), (ethnic + '_ALLELE_FREQ_1')] = str.capitalize(
                    p.readline().replace('\n', ':1'))

    df_working.to_excel("output.xls")