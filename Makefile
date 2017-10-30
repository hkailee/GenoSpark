init: 
	pip install -r requirements.txt

grantPermissions:
	chmod 766 bin/*

downloadVCF:
	bin/download_vcf.sh

buildData:
	bin/buildData.sh

build_SQLite:
	bin/setup_sqlite.py

build_Spark:
	bin/setup_spark.py

#runA:
#	../bin/run.sh -a

# This is a quick check for timming.
# For thorough results, use the profile
# option
#runT:
#	echo "Simple timing analysis. Use the 'profile' option for proper profiling"
#	../bin/run.sh -t

#profile:
#	python3 -m cProfile -s cumtime theFlood.py

#clean:
#	../bin/clean.sh
