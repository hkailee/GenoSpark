#!/usr/bin/env bash

#author = "Hong Kai LEE"
#copyright = "Copyright 2017-2018, Molecular Diagnosis Centre, National University Hospital, Singapore "
#credits = "Bustamin KOSMO, Benjamin CHOR"
#license = "GPL"
#version = "1.0.0"
#maintainer = "Hong Kai LEE"
#email = "hong_kai_lee@nuhs.edu.sg"
#status = "Development"


## helper functions
set -e

## get the params for this run
source bin/genospark_params.sh

#####################
## Download vcf from 1000 Genome database
#####################

## make vcfs storage directory
[ -d $VCF ] || mkdir $VCF

## make vcf storage sub-directory for 1000G
[ -d $VCF/1000G ] || mkdir $VCF/1000G
cd $VCF/1000G

FTP_SITE=ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502                                                       ## tells you which pop and superpop for each sample

## Download the autosomes
for CHR in `seq 1 22`; do
   FILE=$FTP_SITE/ALL.chr$CHR.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
   wget -c $FILE
   sleep 60
done

## Download chromosome X – the filename have v1b instead of v5a like autosomes ##
FILE=$FTP_SITE/ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf.gz
wget -c $FILE


#####################
## Download vcf of Indian population from Singapore Public Health Genomics
#####################

## make vcf storage sub-directory for Singapore Indian
[ -d ../SgIndian ] || mkdir ../SgIndian
cd ../SgIndian

## Download the autosomes and sex chromosomes
wget -c http://phg.nus.edu.sg/StatGen/public_html/SSIP/downloads/vcf.zip
unzip -o vcf.zip


#####################
## Download vcf of Malay population from Singapore Public Health Genomics
#####################

## make vcf storage sub-directory for Singapore Malay
[ -d ../SgMalay ] || mkdir ../SgMalay
cd ../SgMalay

## Download the autosomes and sex chromosomes
wget -c http://phg.nus.edu.sg/StatGen/public_html/SSMP/downloads/vcf.zip
unzip -o vcf.zip
