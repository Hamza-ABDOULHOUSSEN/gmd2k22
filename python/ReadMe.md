# Python INFO

- [Python INFO](#python-info)
  - [Root folder](#root-folder)
  - [Mysql dependencies](#mysql-dependencies)
  - [Requirements](#requirements)
  - [Test](#test)
  - [drugbank package](#drugbank-package)
    - [search](#search)
  - [omim package](#omim-package)
  - [sider package](#sider-package)
  - [stitch package](#stitch-package)


## Root folder
The root folder is this one : `python`  
The commands should be executed from this folder



## Mysql dependencies
You need to install `mysql` dependencies to use mysql package on `python`.

Installation on Mac :
```
brew install mysql
```


## Requirements
Python requirements are in `requirements.txt`  

```
pip install -r requirements.txt
```

## Test
The folder contains a package `test` for tests made with pytest.

To run the tests
```
pytest
```

To run a specific test
```
pytest <file>
```
ex
```
pytest test/test_drugbank_index.py
```


## drugbank package

launch main from `python` folder
```
python3 -m drugbank.drugbank_index_query
```
or
```
python3 -m drugbank.drugbank_index_query "id : DB00005"
```
  

output (for `id : DB0000*`)
```
result : 9
id : DB00001
name : lepirudin
description : Lepirudin is identical to natural hirudin except for substitution of leucine for isoleucine at the N-terminal end of the molecule and the absence of a sulfate group on the tyrosine at position 63. It is produced via yeast cells. Bayer ceased the production of lepirudin (Refludan) effective May 31
indication :  2012.
toxicity : For the treatment of heparin-induced thrombocytopenia
synonyms : In case of overdose (eg
atc_code :  suggested by excessively high aPTT values) the risk of bleeding is increased.

```
### search
This method take a lucene query and do the request into the drugbank index
```
search('id : DB0000*')
```

## omim package
extract omim attributes

## sider package
get sider tables and columns

<span style="color:red">You have to use the school vpn</span>

## stitch package
Launch query in the stitch indexes
as drugbank package
