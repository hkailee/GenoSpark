#!/usr/bin/env python3

__author__ = 'mdc_hk'
version = '1.0'

# Description: To build the database on the pyspark DataFrame
# Usage: -
# Example: -

import datetime, multiprocessing, os, re, shutil, sys, subprocess, time, logging

import pyspark.sql.types as typ
from pyspark.sql.functions import lit
from hdfs import Config


###############
### Creating sql table for the input
###############

xls_file = pd.ExcelFile('query.xlsx')
table = xls_file.parse('All Samples')
# chrom = [x for x in table['Chr'].unique()[:-1]]
conn = sqlite3.connect('dbase_Sqlite')
try:
    cleardb('dbase_Sqlite', 'dataFrame')
except:
    pass
table.to_sql('dataFrame', conn)

###############
### Specify schemas
###############

schema_Freq = typ.StructType([
    typ.StructField("CHROM", typ.IntegerType(), False),
    typ.StructField("POS", typ.IntegerType(), False),
    typ.StructField("N_ALLELES", typ.IntegerType(), False),
    typ.StructField("N_CHR", typ.IntegerType(), False),
    typ.StructField("ALLELE_FREQ_1", typ.StringType(), False),
    typ.StructField("ALLELE_FREQ_2", typ.StringType(), False),
])

schema_rsID = typ.StructType([
    typ.StructField("CHROM", typ.IntegerType(), False),
    typ.StructField("POS", typ.IntegerType(), False),
    typ.StructField("ID", typ.StringType(), True),
])

schema_Freq_DF = typ.StructType([
    typ.StructField("CHROM", typ.IntegerType(), False),
    typ.StructField("POS", typ.IntegerType(), False),
    typ.StructField("N_ALLELES", typ.IntegerType(), False),
    typ.StructField("N_CHR", typ.IntegerType(), False),
    typ.StructField("ALLELE_FREQ_1", typ.StringType(), False),
    typ.StructField("ALLELE_FREQ_2", typ.StringType(), False),
    typ.StructField("ID", typ.StringType(), True),
])

###############
### Setting up File Paths and Lists
###############

client = Config().get_client('dev')

workingFolder_Indian = "SgIndian_vcf/dataFreeze_Feb2013/SNP/biAllele/"

workingFolder_Malay = "SgMalay_vcf/2012_05/snps/"

workingFolder_Chinese = "1000G_CDX/Phase3/integrated/"

# Filing number of unique samples found in the working folder...

freqFiles_Indian = [f for f in client.list(workingFolder_Indian) if re.match(r'chr\d+_analysis_exome\.frq', f)]
rsIDFiles_Indian = [f for f in client.list(workingFolder_Indian) if re.match(r'chr\d+_rsID', f)]
freqFiles_Malay = [f for f in client.list(workingFolder_Malay) if re.match(r'chr\d+_analysis_exome\.frq', f)]
rsIDFiles_Malay = [f for f in client.list(workingFolder_Malay) if re.match(r'chr\d+_rsID', f)]
freqFiles_Chinese = [f for f in client.list(workingFolder_Chinese) if re.match(r'chr\d+_analysis_exome\.frq', f)]
rsIDFiles_Chinese = [f for f in client.list(workingFolder_Chinese) if re.match(r'chr\d+_rsID', f)]

freqFilesID_pre = re.compile(r'(chr\d+)_analysis_exome\.frq')
freqFilesID = []
for file in freqFiles_Indian:
    freqFilesID.append(freqFilesID_pre.findall(file))

print(freqFilesID)