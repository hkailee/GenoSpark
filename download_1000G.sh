 
#############
## Download ##
##############
 
mkdir -p /data/genotypes/1000G/Phase3/integrated && cd $_
 
FTP_SITE=ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502
wget $FTP_SITE/integrated_call_samples_v3.20130502.ALL.panel                                                         ## tells you which pop and superpop for each sample
 
## Download the autosomes ##
for CHR in `seq 1 22`; do
   FILE=$FTP_SITE/ALL.chr$CHR.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
   wget $FILE $FILE.tbi
   sleep 60
done
 
## Download chromosome X – the filenames have v1b instead of v5a like autosomes ##
FILE=$FTP_SITE/ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf.gz
wget $FILE $FILE.tbi
 
#rename -v 's/v1b/v5a/' *                                                                                                                            ## rename for convenience later
 
 
 
 
 
