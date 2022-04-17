#!/bin/bash

java -cp ./lib/lucene-analyzers-common-8.4.1.jar:./lib/lucene-core-8.4.1.jar:./lib/lucene-queryparser-8.4.1.jar:./out/production/Drugbank_index Request "$1"