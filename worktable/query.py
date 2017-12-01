#!/usr/bin/env python3
__author__ = 'Hong Kai LEE, Bustamin Kosmo, Benjamin Chor'
version = '1.0'
##==========================================
import datetime, os, subprocess, sys, time, logging
import pandas as pd
#from utils import logDecorator as lD
##==========================================
##Functions:
# 1: Checks if in proper number of arguments are passed gives instructions on proper use.
def argsCheck(numArgs):
	if len(sys.argv) < numArgs or len(sys.argv) > numArgs:
		print('GenoSpark version 1.0')
		print('Usage:', sys.argv[0], '<Input Filename>',' <Output Filename>')
		print('Examples:', sys.argv[0], 'input.xls', 'output,xls')
		exit(1) # Aborts program. (exit(1) indicates that an error occurred)
#===========================================================================================================
# Housekeeping.
argsCheck(3) # Checks if the number of arguments are correct.

# Stores file one for input checking.
inFile  = sys.argv[1]
outFile = sys.argv[2]

# Working environment/directory configuration
sys.path.append(os.path.abspath('..'))
workingFolder = os.getcwd()
if not os.path.exists(workingFolder + '/Logs'):
    os.makedirs(workingFolder + '/Logs')

# Logging events...
logging.basicConfig(filename=workingFolder + '/Logs/log_' + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Command-line invocation: ' + sys.argv[0] + ' ' + sys.argv[1] + ' ' + sys.argv[2])
logging.info('Runfolder path: ' + workingFolder)

if __name__ == '__main__':
    from bin.utils.createDB import *

    if not os.path.exists(workingFolder + '/results'):
        os.makedirs(workingFolder + '/results')
        logging.info('A "results" directory created. All outputs will be stored in this directory')
    ###=================================
    ### Creating sql table for the input
    ###=================================

    xls_file = pd.ExcelFile(inFile)
    table = xls_file.parse('Sheet1')
    conn = sqlite3.connect('../dbase_Sqlite')
    cleardb('../dbase_Sqlite', 'dataFrame')
    table.to_sql('dataFrame', conn)
    logging.info('Query input table inserted as sql table.')

    ###====================================================
    ### Querying from Chinese, Malay and Indian populations
    ###====================================================

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
          '- Data Retrieval for all races completing (1/2): Took {} seconds.'.format(timeTaken))
    logging.info('Data Retrieval for all races completing (1/2): Took {} seconds.'.format(timeTaken))

    df_working = df[:]

    startTime = time.time()

    for ethnic in ['Indian', 'Malay', 'Chinese']:
        df_Null_temp = df_working[df_working[ethnic + "_ALLELE_FREQ_1"].isnull()]
        for chrom in df_Null_temp.CHROM.unique():
            if not chrom == None:
                df_Null_temp_working = df_Null_temp[(df_Null_temp.Chr.astype(str) == str(chrom))]
                with open('query.bed', 'w') as bedFile:
                    for i in df_Null_temp_working['Coordinate']:
                        bedFile.write('chr' + str(chrom) + '\t' + str(i - 1) + '\t' + str(i) + '\n')
                with open('output.fa', 'w') as outfile:
                    proc = subprocess.Popen(['seqtk', 'subseq', '../data/GRCh37/chr' + str(chrom) + '.fa', 'query.bed'],
                                        stdin=subprocess.PIPE, stdout=outfile)
                    out, err = proc.communicate()

                p = open('output.fa', "r")
                for i in df_Null_temp_working.index:
                    p.readline()
                    df_working.loc[(df_working.index == i), (ethnic + '_ALLELE_FREQ_1')] = str.capitalize(
                        p.readline().replace('\n', ':1'))

    df_working.to_excel('results/' + outFile)

    timeTaken = time.time()-startTime
    print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
          '- Data Retrieval for all races completed (2/2): Took {} seconds to complete.'.format(timeTaken))
    logging.info('Data Retrieval for all races completed (2/2): Took {} seconds to complete.'.format(timeTaken))
