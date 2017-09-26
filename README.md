# What's GenoSpark about?

**GenoSpark** is a tool that queries the population genetic frequency of three major ethnics in Singapore 
on a Apache Spark framework running on top of Hadoop (Distributed filesystem). The current version of GenoSpark (v1.0, October 2017) 
has a separate local SQLite version (i.e. Job performed on the usual local filesystem).

<hr>

## Changelog

### Version 1.0.0
The initial version

<hr>

# Getting Started

## Requirements

**GenoSpark** was designed to run on Linux systems. It can run in OSX too (tested only in Sierra). 
It depends on the following programs to function:

[VCFtools](https://vcftools.github.io/downloads.html) (version 0.1.15)
[bcftools](http://www.htslib.org/download/) (version 1.5, using htslib 1.5)

