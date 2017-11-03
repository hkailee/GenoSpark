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
    table = xls_file.parse('All Samples')
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

    print('There are', multiprocessing.cpu_count(), 'cpu\'s available in this machine')

    responses={}
    responses_lock=threading.Lock()

    maxconnections = multiprocessing.cpu_count()
    pool_sema = BoundedSemaphore(value=maxconnections)

    def task(fname):
        pool_sema.acquire()
        conn = sqlite3.connect('../dbase_Sqlite')
        if fname != 'Chinese':
            query = """
                SELECT DISTINCT
                    dataFrame.*, """ + fname + """_ALLELE_FREQ_1, """ + fname + """_ALLELE_FREQ_2, """ + fname + """.ID
                FROM
                    dataFrame LEFT OUTER JOIN 
                    """ + fname + """ ON dataFrame.Coordinate=""" + fname + """.POS 
                AND dataFrame.Chr=""" + fname + """.CHROM
                """
        else:
            query = """
                SELECT DISTINCT
                    dataFrame.*, """ + fname + """_ALLELE_FREQ_1, """ + fname + """_ALLELE_FREQ_2, """ + fname + """_ALLELE_FREQ_3, """ + fname + """_ALLELE_FREQ_4, """ + fname + """.ID
                FROM
                    dataFrame LEFT OUTER JOIN 
                    """ + fname + """ ON dataFrame.Coordinate=""" + fname + """.POS 
                AND dataFrame.Chr=""" + fname + """.CHROM
                """
        df = pd.read_sql_query(query , conn)
        conn.close()
        pool_sema.release()
        responses_lock.acquire()
        responses[fname] = df
        responses_lock.release()

    pool = []

    #find sql files and spawn theads
    for fname in ['Chinese', 'Indian', 'Malay']:
        #create new thread with task
        thread = threading.Thread(target=task,args=(fname,))
        thread.daemon = True
        # store thread in pool
        pool.append(thread)
        #thread started
        thread.start()

    #wait for all threads tasks done
    for thread in pool:
        thread.join()

    timeTaken = time.time()-startTime
    print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
          '- Data Retrieval for all races completed: Took {} seconds to complete.'.format(timeTaken))


    ################
    ### Merging the output tables into one table
    ################

    df_M = responses['Malay']
    df_I = responses['Indian']
    df_C = responses['Chinese']
    df = df_I.merge(df_C[['index','Chinese_ALLELE_FREQ_1','Chinese_ALLELE_FREQ_2','Chinese_ALLELE_FREQ_3', 'Chinese_ALLELE_FREQ_4']],
                    on=['index'], how='outer').merge(df_M[['index','Malay_ALLELE_FREQ_1', 'Malay_ALLELE_FREQ_2']], on=['index'], how='outer')


    df_working = df[:]

    for ethnic in ['Indian', 'Malay', 'Chinese']:
        df_Null_temp = df_working[df_working[ethnic + "_ALLELE_FREQ_1"].isnull()]
        for chrom in list(range(1, 23)) + ['X']:
            df_Null_temp_working = df_Null_temp[(df_Null_temp.Chr == str(chrom))]
            with open('query.bed', 'w') as bedFile:
                for i in df_Null_temp_working['Coordinate']:
                    bedFile.write('chr' + str(chrom) + '\t' + str(i - 1) + '\t' + str(i) + '\n')
            with open('output.fa', 'w') as outfile:
                proc = subprocess.Popen(['seqtk', 'subseq', '../../GRCh37/chr' + str(chrom) + '.fa', 'query.bed'],
                                        stdin=subprocess.PIPE, stdout=outfile)
                out, err = proc.communicate()

            p = open('output.fa', "r")
            for i in df_Null_temp_working.index:
                p.readline()
                df_working.loc[(df_working.index == i), (ethnic + '_ALLELE_FREQ_1')] = str.capitalize(
                    p.readline().replace('\n', ':1'))

    df_working.to_excel("output.xls")