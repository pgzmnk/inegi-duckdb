# INEGI

- INEGI administrative boundaries
- INEGI zonas metropolitanas
- DENUE

## Walkthrough

### Download 2020 administrative boundaries
https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469/889463807469_s.zip

### Transform shapefiles to parquets
```
python3  run.py data/MG_2020_Integrado/conjunto_de_datos/00ent.shp tmp/00ent.parquet
python3  run.py data/MG_2020_Integrado/conjunto_de_datos/00mun.shp tmp/00mun.parquet
python3  run.py data/MG_2020_Integrado/conjunto_de_datos/00a.shp tmp/00a.parquet
```

### Read into duckdb
```sql
CREATE TABLE ent AS SELECT * FROM 'tmp/00ent.parquet';
CREATE TABLE mun AS SELECT * FROM 'tmp/00mun.parquet';
CREATE TABLE ageb AS SELECT * FROM 'tmp/00a.parquet';
```