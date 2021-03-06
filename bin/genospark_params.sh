#!/usr/bin/env bash

#author = "Hong Kai LEE"
#copyright = "Copyright 2017, Molecular Diagnosis Centre, National University Hospital, Singapore "
#credits = "Bustamin KOSMO, Benjamin CHOR"
#license = "GPL"
#version = "1.0.0"
#maintainer = "Hong Kai LEE"
#email = "hong_kai_lee@nuhs.edu.sg"
#status = "Development"

#######################
## GenoSpark parameters. REVIEW BEFORE RUNNING THE PIPELINE.
#######################

#Prefix for the output files.
PREFIX=output

#Directory for storage of all vcfs.
VCF=vcf/

#Directory for storage of indian's vcfs
VCFMalay=vcf/SgMalay/vcf/2012_05/snps

#File name of the 1000G samplelist
CHX_LIST=1000G_CHX.txt

#Directory to place resulting files.
RESULTS=results/

#Maximum number of processors to be requested.
NPROC=4

#Name of the GZip executable. If you have pigz (parallel gzip), enter it here.
#For example: GZIP="pigz -p $NPROC"
GZIP=gz