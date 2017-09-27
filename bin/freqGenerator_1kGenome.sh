#!/usr/bin/env bash
## vcftools freq the autosomes ##
for CHR in {1..22} 
do

    FILE=ALL.chr$CHR.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
    vcftools --gzvcf $FILE --freq --chr $CHR --out chr${CHR}_analysis --keep sampleslist.txt

done

## bcftools query the autosomes ##

for CHR in {1..22}
do

    FILE=ALL.chr$CHR.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
    bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o chr${CHR}_rsID

done

## vcftools freq chromosome X – the filenames have v1b instead of v5a like autosomes ##
#FILE=ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf.gz
#vcftools --gzvcf $FILE --freq --chr X --out chrX_1k_analysis

## bcftools query chromosome X – the filenames have v1b instead of v5a like autosomes ##
#FILE=ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf.gz
#bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o chrX_1k_rsID
