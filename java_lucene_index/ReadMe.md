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
  - [Stitch br08303](#stitch-br08303)
    - [Fields](#fields-2)
    - [Queries](#queries-2)
    - [Bash script launcher](#bash-script-launcher-2)
  - [Hpo](#hpo)
    - [Fields](#fields-3)
    - [Queries](#queries-3)
    - [Bash script launcher](#bash-script-launcher-3)


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

## Stitch br08303
### Fields
- atc_code
- drug_name

### Queries
example of queries
```
atc_code : B01AE02
```
```
drug_name : Lepirudin
```

### Bash script launcher
```
./launch.sh stitch.br08303 <query>
```

ex :
```
./launch.sh stitch.br08303 "atc_code : B01AE02"
```

## Hpo
### Fields
- hpo_id
- symptom
- synonyms
- is_a

### Queries
example of queries
```
hpo_id : HP_0000045
```
```
symptom: Abnormality of the scrotum
```

### Bash script launcher
```
./launch.sh hpo <query>
```

ex :
```
./launch.sh hpo "hpo_id : HP_0000045"
```
