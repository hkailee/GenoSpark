import os, sqlite3, time, datetime, subprocess
import pandas as pd
import multiprocessing
import threading
from threading import BoundedSemaphore
from utils import logDecorator as lD

from utils.createDB import *
from utils.query import *


@lD.log('simpleQuery')
def simpleQuery(logger, ethnic):

    try:
        conn = sqlite3.connect('../dbase_Sqlite')
    except Exception as e:
        logger.error('Unable to connect to the database: {}: \n{}'.format(
            'dbase_Sqlite'), str(e))
        return

    try:
        if not ethnic == "Chinese":
            data = None
            query = '''
            SELECT DISTINCT
                dataFrame.*, ''' + ethnic + '''_ALLELE_FREQ_1, ''' + ethnic + '''_ALLELE_FREQ_2, ''' + ethnic + '''.ID
            FROM
                dataFrame LEFT OUTER JOIN 
                ''' + ethnic + ''' ON dataFrame.Coordinate=''' + ethnic + '''.POS 
                AND dataFrame.Chr=''' + ethnic + '''.CHROM
            '''
        else:
            data = None
            query = '''
            SELECT DISTINCT
                dataFrame.*, ''' + ethnic + '''_ALLELE_FREQ_1, ''' + ethnic + '''_ALLELE_FREQ_2, ''' + \
                    ethnic + '''_ALLELE_FREQ_3, ''' + ethnic + '''_ALLELE_FREQ_4, ''' + ethnic + '''.ID
            FROM
                dataFrame LEFT OUTER JOIN 
                ''' + ethnic + ''' ON dataFrame.Coordinate=''' + ethnic + '''.POS 
                AND dataFrame.Chr=''' + ethnic + '''.CHROM
            '''
        data = pd.read_sql_query(query , conn)
        logger.info('Query: \n{}\n  --> returned {} values'.format(query, len(data)))
    except Exception as e:
        logger.error('Unable to perform the query: {}\n{}'.format(
            query, str(e)))

    try:
        conn.close()
    except Exception as e:
        logger.error('Unable to close the connection for some reason')

    return data

@lD.logInit('Main')
def main(logger):
    xls_file = pd.ExcelFile('../query.xlsx')
    table = xls_file.parse('All Samples')
    chrom = [x for x in table['Chr'].unique()[:-1]]
    conn = sqlite3.connect('../dbase_Sqlite')
    try:
        cleardb('../dbase_Sqlite', 'dataFrame')
    except Exception as e:
        logger.error('Unable to do query: \n{}'.format(str(e)))
    table.to_sql('dataFrame', conn)
    
    try:
        df_M = simpleQuery('Malay')
        df_M = simpleQuery('Indian')
        df_C = simpleQuery('Chinese')

        print(df_M[:10])
    except:
        pass

if __name__ == '__main__':
    main()