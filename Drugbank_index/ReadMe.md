# Drugbank index

## Dependencies
Lucene dependencies

## Fields
- id
- name
- description
- indication
- toxicity
- synonyms
- atc_code

## Queries
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

## Bash script launcher
```
./launch.sh <query>
```

ex :
```
./launch.sh "id : DB00001"
```