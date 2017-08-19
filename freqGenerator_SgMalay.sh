## vcftools freq the autosomes ##
for CHR in {1..22} 
do

    FILE=SSM.chr$CHR.2012_05.genotypes.vcf.gz
    vcftools --gzvcf $FILE --freq --chr $CHR --out chr${CHR}_analysis

done

## bcftools query the autosomes ##

for CHR in {1..22}
do

    FILE=SSM.chr$CHR.2012_05.genotypes.vcf.gz
    bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o chr${CHR}_rsID

done

## vcftools freq chromosome X – the filenames have v1b instead of v5a like autosomes ##
FILE=SSM.chrX.2012_05.genotypes.vcf.gz
vcftools --gzvcf $FILE --freq --chr X --out chrX_analysis
bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o chrX_rsID

## bcftools query chromosome X – the filenames have v1b instead of v5a like autosomes ##
FILE=SSM.chrY.2012_05.genotypes.vcf.gz
vcftools --gzvcf $FILE --freq --chr Y --out chrY_analysis
bcftools query -f '%CHROM\t%POS\t%ID\n' $FILE -o chrY_rsID
