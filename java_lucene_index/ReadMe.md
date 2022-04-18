# Lucene Index

- [Lucene Index](#lucene-index)
  - [Dependencies](#dependencies)
  - [Drugbank](#drugbank)
    - [Fields](#fields)
    - [Queries](#queries)
    - [Bash script launcher](#bash-script-launcher)
  - [Stitch chemical sources](#stitch-chemical-sources)
    - [Fields](#fields-1)
    - [Queries](#queries-1)
    - [Bash script launcher](#bash-script-launcher-1)


## Dependencies
Lucene dependencies

## Drugbank
### Fields
- id
- name
- description
- indication
- toxicity
- synonyms
- atc_code

### Queries
example of queries
```
id : DB00001
```

```
id : DB0000*
```

```
status:[400 TO *]
```

```
name : lepirudin AND (id : DB00001 OR id : DB00002)
```

### Bash script launcher
```
./launch.sh drugbank <query>
```

ex :
```
./launch.sh drugbank "id : DB00001"
```

## Stitch chemical sources
### Fields
- chemical
- alias
- source_format
- source_code

### Queries
example of queries
```
source_format : ATC
```

### Bash script launcher
```
./launch.sh stitch.chemical_sources <query>
```

ex :
```
./launch.sh stitch.chemical_sources "source_format : ATC"
```