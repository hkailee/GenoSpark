#!/usr/bin/env bash

#author = "Hong Kai LEE"
#copyright = "Copyright 2017, Molecular Diagnosis Centre, National University Hospital, Singapore "
#credits = "Bustamin KOSMO, Benjamin CHOR"
#license = "GPL"
#version = "1.0.0"
#maintainer = "Hong Kai LEE"
#email = "hong_kai_lee@nuhs.edu.sg"
#status = "Development"

#helper functions
set -e

#die function
warn () {
    echo "$0:" "$@" >&2
}
die () {
    rc=$1
    shift
    warn "$@"
    exit $rc
}

isitthere () {
  [ -s $1 ] || die 1 "File $1 not found or zero sized."
}

#get the params for this run
source genospark_params.sh

##################################
### Chinese Frequency Generation
##################################

## make Chinese frequency folder ##
[ -d ../data/Chinese ] || mkdir ../data/Chinese
isitthere ../data/$CHX_LIST
isitthere ../vcf/1000G

## vcftools and bcftools query the autosomes ##
for CHR in {1..22}
do
    FILE=../vcf/1000G/ALL.chr$CHR.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
    vcftools --gzvcf $FILE --freq --chr $CHR --out ../data/Chinese/chr${CHR}_analysis --keep ../data/$CHX_LIST
    bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o ../data/Chinese/chr${CHR}_rsID
done

## vcftools freq chromosome X – the filenames have v1b instead of v5a like autosomes ##
FILE=../vcf/1000G/ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf.gz
vcftools --gzvcf $FILE --freq --chr X --out ../data/Chinese/chrX_analysis
bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o ../data/Chinese/chrX_rsID

## bcftools query chromosome Y – the filenames have v1b instead of v5a like autosomes ##
FILE=../vcf/1000G/ALL.chrY.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf.gz
vcftools --gzvcf $FILE --freq --chr Y --out ../data/Chinese/chrY_analysis
bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o ../data/Chinese/chrY_rsID


##################################
### Malay Frequency Generation
##################################

## make Malay frequency folder
[ -d ../data/Malay ] || mkdir ../data/Malay
isitthere ../vcf/SgMalay/vcf/2012_05/snps

## vcftools and bcftools query the autosomes ##
for CHR in {1..22}
do
    FILE=../vcf/SgMalay/vcf/2012_05/snps/SSM.chr$CHR.2012_05.genotypes.vcf.gz
    vcftools --gzvcf $FILE --freq --chr $CHR --out ../data/Malay/chr${CHR}_analysis
    bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o ../data/Malay/chr${CHR}_rsID

done

## vcftools freq chromosome X – the filenames have v1b instead of v5a like autosomes ##
FILE=../vcf/SgMalay/vcf/2012_05/snps/SSM.chrX.2012_05.genotypes.vcf.gz
vcftools --gzvcf $FILE --freq --chr X --out ../data/Malay/chrX_analysis
#bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o ../data/Malay/chrX_rsID

## bcftools query chromosome Y – the filenames have v1b instead of v5a like autosomes ##
FILE=../vcf/SgMalay/vcf/2012_05/snps/SSM.chrY.2012_05.genotypes.vcf.gz
vcftools --gzvcf $FILE --freq --chr Y --out ../data/Malay/chrY_analysis
#bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o ../data/Malay/chrY_rsID


##################################
### Indian Frequency Generation
##################################

## make Malay frequency folder
[ -d ../data/Indian ] || mkdir ../data/Indian
isitthere ../vcf/SgIndian/vcf/dataFreeze_Feb2013/SNP/biAllele

## vcftools and bcftools query the autosomes ##
for CHR in {1..22}
do
    FILE=../vcf/SgIndian/vcf/dataFreeze_Feb2013/SNP/biAllele/chr$CHR.consolidate.eff.PPH.vcf.gz
    vcftools --gzvcf $FILE --freq --chr $CHR --out ../data/Indian/chr${CHR}_analysis
    bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o ../data/Indian/chr${CHR}_rsID

done

## vcftools freq chromosome X – the filenames have v1b instead of v5a like autosomes ##
FILE=../vcf/SgIndian/vcf/dataFreeze_Feb2013/SNP/biAllele/chrX.consolidate.eff.PPH.vcf.gz
vcftools --gzvcf $FILE --freq --chr X --out ../data/Indian/chrX_analysis
bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o ../data/Indian/chrX_rsID

## bcftools query chromosome Y – the filenames have v1b instead of v5a like autosomes ##
FILE=../vcf/SgIndian/vcf/dataFreeze_Feb2013/SNP/biAllele/chrY.consolidate.eff.PPH.vcf.gz
vcftools --gzvcf $FILE --freq --chr Y --out ../data/Indian/chrY_analysis
bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o ../data/Indian/chrY_rsID
