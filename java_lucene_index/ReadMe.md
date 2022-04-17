# Lucene Index

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