#!/usr/bin/env python3

import datetime, logging, os, re, subprocess, time
from utils.createDB import *

##################
### Administration
##################
logging.basicConfig(filename= 'log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

workingFolder_Indian = "data/Indian/"

workingFolder_Malay = "data/Malay/"

workingFolder_Chinese = "data/Chinese/"

# Filing number of unique samples found in the working folder...

freqFiles_Indian = [f for f in os.listdir(workingFolder_Indian) if re.match(r'chr[A-Z0-9]+_analysis\.frq', f)]
rsIDFiles_Indian = [f for f in os.listdir(workingFolder_Indian) if re.match(r'chr[A-Z0-9]+_rsID', f)]
freqFiles_Malay = [f for f in os.listdir(workingFolder_Malay) if re.match(r'chr[A-Z0-9]+_analysis\.frq', f)]
rsIDFiles_Malay = [f for f in os.listdir(workingFolder_Malay) if re.match(r'chr[A-Z0-9]+_rsID', f)]
freqFiles_Chinese = [f for f in os.listdir(workingFolder_Chinese) if re.match(r'chr[A-Z0-9]+_analysis\.frq', f)]
rsIDFiles_Chinese = [f for f in os.listdir(workingFolder_Chinese) if re.match(r'chr[A-Z0-9]+_rsID', f)]

freqFilesID_pre = re.compile(r'(chr[A-Z0-9]+)_analysis\.frq')
freqFilesID = []
for file in freqFiles_Indian:
    freqFilesID.append(freqFilesID_pre.findall(file))

####################
### For Malay Data and rsID
####################

startTime = time.time()
########
makedb('dbase_Sqlite', 'Malay_Data', "(CHROM int(2), POS int(10), N_ALLELES int(1), N_CHR int(4), Malay_ALLELE_FREQ_1 char(30), Malay_ALLELE_FREQ_2 char(30))")
########
for ID in freqFilesID:
    loaddb('Malay_Data', 'dbase_Sqlite', workingFolder_Malay + ID[0] +'_analysis.frq')
    logging.info('Inserting values from ' +  workingFolder_Malay + ID[0] + '_analysis.frq ' +
                 'to Malay_Data table of dbase_Sqlite database')
timeTaken = time.time()-startTime
print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
      '- Data Loading for Malay_Data table of dbase_Sqlite database completed: Took {} '
      'seconds to complete.'.format(timeTaken))

## Parsing the Malay vcf manually to generate rsID table
## >>> created only for the Singapore Malay vcf as command below produced error as such::
##    $ bcftools query -f '%CHROM\t%POS\t%ID\n' SSM.chr8.2012_05.genotypes.vcf.gz -o chr8_rsID
##    $ [E::bcf_hdr_add_sample] Empty sample name: trailing spaces/tabs in the header line?

## to gunzip vcf.gz for Malay only
startTime = time.time()
for ID in freqFilesID:
    try:
        proc1 = subprocess.Popen(['gunzip', '-k', 'vcf/SgMalay/vcf/2012_05/snps/' + 'SSM.' + ID[0] + '.2012_05.genotypes.vcf.gz'],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = proc1.communicate()
        logging.info('gunzip ' + 'vcf/SgMalay/vcf/2012_05/snps/' + 'SSM.' + ID[0] + '.2012_05.genotypes.vcf.gz')
    except:
        logging.info('vcf/SgMalay/vcf/2012_05/snps/' + 'SSM.' + ID[0] + '.2012_05.genotypes.vcf.gz not present')
        pass
timeTaken = time.time()-startTime
print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
      '- gunzip completed: Took {} seconds to complete.'.format(timeTaken))

# Manually load data from a raw vcf for Malay population only
startTime = time.time()
########
makedb('dbase_Sqlite', 'Malay_rsID', "(CHROM int(2), POS int(10), ID char(15))")
########
for ID in freqFilesID:
    loaddb_vcf_rsID('Malay_rsID', 'dbase_Sqlite', 'vcf/SgMalay/vcf/2012_05/snps/' + 'SSM.' + ID[0] + '.2012_05.genotypes.vcf')
    logging.info('Inserting values from ' +  'vcf/SgMalay/vcf/2012_05/snps/'  + 'SSM.' + ID[0] +
                 '.2012_05.genotypes.vcf to Malay_rsID table of dbase_Sqlite database')
timeTaken = time.time()-startTime
print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
      '- Data Loading for Malay_rsID of dbase_Sqlite database completed: Took {} seconds to complete.'.format(timeTaken))

####################
### For Indian Data and rsID
####################

startTime = time.time()

########
makedb('dbase_Sqlite', 'Indian_Data', "(CHROM int(2), POS int(10), N_ALLELES int(1), N_CHR int(4), Indian_ALLELE_FREQ_1 char(30), Indian_ALLELE_FREQ_2 char(30))")
########
for ID in freqFilesID:
    loaddb('Indian_Data', 'dbase_Sqlite', workingFolder_Indian + ID[0] +'_analysis.frq')
    logging.info('Inserting values from ' +  workingFolder_Indian + ID[0] + '_analysis.frq ' +
                 'to Indian_Data table of dbase_Sqlite database')
timeTaken = time.time()-startTime
print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
      '- Data Loading for Indian_Data table of dbase_Sqlite database completed: Took {} '
      'seconds to complete.'.format(timeTaken))

########
makedb('dbase_Sqlite', 'Indian_rsID', "(CHROM int(2), POS int(10), ID char(15))")
########
for ID in freqFilesID:
    loaddb('Indian_rsID', 'dbase_Sqlite', workingFolder_Indian + ID[0] +'_rsID')
    logging.info('Inserting values from ' +  workingFolder_Indian + ID[0] + '_rsID ' +
                 'to Indian_rsID table of dbase_Sqlite database')
timeTaken = time.time()-startTime
print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
      '- Data Loading for Indian_rsID table of dbase_Sqlite database completed: Took {} '
      'seconds to complete.'.format(timeTaken))

####################
### For Chinese Data and rsID
####################

startTime = time.time()
######
query_Data = "(CHROM int(2), POS int(10), N_ALLELES int(1), N_CHR int(4), Chinese_ALLELE_FREQ_1 char(50), Chinese_ALLELE_FREQ_2 char(50), Chinese_ALLELE_FREQ_3 char(50), Chinese_ALLELE_FREQ_4 char(50))"
makedb('dbase_Sqlite', 'Chinese_Data', query_Data)
######
for ID in freqFilesID:
    loaddb_chineseData('Chinese_Data', 'dbase_Sqlite', workingFolder_Chinese + ID[0] +'_analysis.frq')
    logging.info('Inserting values from ' +  workingFolder_Chinese + ID[0] + '_analysis.frq ' +
                 'to Chinese_Data table of dbase_Sqlite database')
timeTaken = time.time()-startTime
print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
      '- Data Loading for Chinese_Data table of dbase_Sqlite database completed: Took {} '
      'seconds to complete.'.format(timeTaken))

######
makedb('dbase_Sqlite', 'Chinese_rsID', '(CHROM int(2), POS int(10), ID chr(15))')
#######
for ID in freqFilesID:
    loaddb('Chinese_rsID', 'dbase_Sqlite', workingFolder_Chinese + ID[0] +'_rsID')
    logging.info('Inserting values from ' +  workingFolder_Chinese + ID[0] + '_rsID ' +
                 'to Chinese_rsID table of dbase_Sqlite database')
timeTaken = time.time()-startTime
print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
      '- Data Loading for Chinese_rsID table of dbase_Sqlite database completed: Took {} '
      'seconds to complete.'.format(timeTaken))

####################
### Create combined tables (Data + rsID) for Malay, Indian, and Chinese
####################

## Malay
query = '''SELECT 
                Malay_Data.CHROM, 
                Malay_Data.POS, 
                N_ALLELES, 
                N_CHR, 
                Malay_ALLELE_FREQ_1, 
                Malay_ALLELE_FREQ_2, 
                Malay_rsID.ID 
            FROM 
                Malay_Data 
            INNER JOIN 
                Malay_rsID 
            ON 
                Malay_Data.POS = Malay_rsID.POS'''

combinetables('dbase_Sqlite', 'Malay',  query)


# Indian
query = '''SELECT 
                Indian_Data.CHROM, 
                Indian_Data.POS, 
                N_ALLELES, 
                N_CHR, 
                Indian_ALLELE_FREQ_1, 
                Indian_ALLELE_FREQ_2, 
                Indian_rsID.ID 
            FROM 
                Indian_Data 
            INNER JOIN 
                Indian_rsID 
            ON 
                Indian_Data.POS = Indian_rsID.POS'''

combinetables('dbase_Sqlite', 'Indian',  query)

## Chinese
query = '''SELECT 
                Chinese_Data.CHROM, 
                Chinese_Data.POS, 
                N_ALLELES, 
                N_CHR, 
                Chinese_ALLELE_FREQ_1, 
                Chinese_ALLELE_FREQ_2, 
                Chinese_ALLELE_FREQ_3,
                Chinese_ALLELE_FREQ_4,
                Chinese_rsID.ID 
            FROM 
                Chinese_Data 
            INNER JOIN 
                Chinese_rsID 
            ON 
                Chinese_Data.POS = Chinese_rsID.POS'''

combinetables('dbase_Sqlite', 'Chinese',  query)

####################
### Drop unneccessary race_Data and race_rsID tables
####################

cleardb('dbase_Sqlite', 'Malay_Data')
cleardb('dbase_Sqlite', 'Malay_rsID')
cleardb('dbase_Sqlite', 'Indian_Data')
cleardb('dbase_Sqlite', 'Indian_rsID')
cleardb('dbase_Sqlite', 'Chinese_Data')
cleardb('dbase_Sqlite', 'Chinese_rsID')
