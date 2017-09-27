# What's GenoSpark about?

**GenoSpark** is a tool that queries the population genetic frequency of three major ethnics in Singapore 
on a Apache Spark framework running on top of Hadoop (Distributed filesystem). The current version of GenoSpark (v1.0, October 2017) 
has a separate local SQLite version (i.e. Job performed on the usual local filesystem).

The genomes included were:

| Population Label | Population | Individuals | Data Source | 
| ---------------- | ---------- | ----------- | ----------- |
| CDX | Chinese | 93 | 1000 Genomes Project Phase3 | 
| MAS | Malay | 100 | Singapore Public Heath Genomics SSMP |
| INS | Indian | 38 | Singapore Public Heath Genomics SSIP |


<hr>

## Changelog

### Version 1.0.0 (Oct 2017)
The initial version

<hr>

# Getting Started

## Requirements

**GenoSpark** was designed to run on Linux systems. It can run in OSX too (tested only in Sierra). 
It depends on the following sofware to function:

[VCFtools](https://vcftools.github.io/downloads.html) (version 0.1.15)  
[bcftools](http://www.htslib.org/download/) (version 1.5, using htslib 1.5)  
python (version 3.5 or higher)

And the following python 3 libraries are required:

pyspark  
pandas  
hdfs  

Before installing, please make sure all software are installed and their commands in the PATH, and the 
respective python libraries available to the interpreter.  

Be careful of software you may have installed that bundles their own python interpreter, 
as they will most likely conflict with **GenoSpark**'s operation due to missing libraries. 

## Building

The default way to build GenoSpark is:

```
$ git clone https://github.com/hkailee/GenoSpark.git  
$ cd GenoSpark 
```