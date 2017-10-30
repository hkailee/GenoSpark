#!/usr/bin/env python3

import datetime, multiprocessing, logging, os, re, shutil, sys, sqlite3, subprocess, time
import pandas as pd
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

