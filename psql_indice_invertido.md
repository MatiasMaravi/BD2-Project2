# Búsqueda de texto en PostgreSQL

PostgreSQL se refiere a esta actividad como una  especialización para buscar dentro de varios documentos escritos en lenguaje humano aquellas palabras que coincidan con la consulta realizada. Además, nos proporciona dos tipos de datos diseñados para realizar este tipo de búsqueda: `ts_vector` y `ts_query`.

## ts_vector
Consiste en una lista ordenada de lexemas distintos pertenecientes a un documento o una frase en específico. Además, dentro de este vector, se omiten aquellos valores duplicados y elimina aquellas palabras que no aportan ningún valor a la consulta (stopwords). A continuación, se mostrará la sintaxis de esta función:
```sql
SELECT to_tsvector('english',
       'a Fat  Cat sat on a mat - it ate a fat rats');

                     to_tsvector
 -----------------------------------------------------
 'ate':9 'cat':3 'fat':2,11 'mat':7 'rat':12 'sat':4
```
Como se puede observar en la sintaxis, es necesario dar como parámetro el lenguaje del documento o frase ya que obtendrá los lexemas dependiendo del idioma. Cabe resaltar que el idioma por defecto de esta funcionalidad es el inglés. Sin embargo, se puede especificar el idioma en el primer parámetro.

## ts_query
Almacena aquellos lexemas que se van a consultar. Además, se pueden utilizar operadores booleanos: `AND(&)`, `OR(|)` y `NOT(!)`, dentro de estas consultas. También, se puede incluir el operador para búsqueda de frases `FOLLOWED BY(<->)`. Cabe resaltar que se pueden agrupar estos operadores mediante paréntesis y que no es necesario especificar el idioma de la palabra o frase a consultar. A continuación, mostraré un ejemplo de sintaxis:
```sql
SELECT title
 FROM pgweb
 WHERE to_tsvector(body) @@ to_tsquery('friend');
```
En este ejemplo, podemos observar que se buscará la palabra o derivados de 'friend' dentro del ts_vector del atributo 'body'.

# Creación de la base de datos
Para la experimentación necesitaremos extraer la información del archivo csv llamado `spotify_songs`. Esto lo lograremos con el siguiente comando:
```sql
DROP TABLE IF EXISTS spotify_songs;

CREATE TABLE spotify_songs (
	track_id text PRIMARY KEY,
	track_name text ,
	track_artist text,
	lyrics text,
	track_popularity float,
	track_album_id text,
	track_album_name text,
	track_album_release_date text,
	playlist_name text,
	playlist_id text,
	playlist_genre text,
	playlist_subgenre text,
	danceability float,
	energy float,
	key float,
	loudness float,
	mode float,
	speechiness float,
	acousticness float,
	instrumentalness float,
	liveness float,
	valence float,
	tempo float,
	duration_ms float,
	language text
);

COPY spotify_songs(track_id,track_name, track_artist, 
				   lyrics,track_popularity, track_album_id,
				   track_album_name, track_album_release_date,
				   playlist_name,playlist_id,playlist_genre,
				  playlist_subgenre,danceability,energy,key,loudness,
				   mode,speechiness,acousticness,instrumentalness,
				   liveness, valence, tempo,duration_ms,language
				  )
FROM '$YOUR_CSV_PATH$' DELIMITER ',' CSV HEADER;
```
Si bien podemos consultar en todas las canciones disponibles, esto sería muy confuso ya que aplicarían lexemas sobre un lenguaje diferente al idioma de la consulta. Es por esto que decidimos crear otras dos tablas que contengan los dos idiomas que contengan la mayor cantidad de canciones del CSV: inglés y español.
```sql
-- Creando tabla para dos idiomas: Inglés y Español
DROP TABLE IF EXISTS spotify_en;

CREATE TABLE spotify_en AS
SELECT * FROM spotify_songs
WHERE language = 'en';

DROP TABLE IF EXISTS spotify_es;

CREATE TABLE spotify_es AS
SELECT * FROM spotify_songs
WHERE language = 'es';
```
Ahora, con los datos proporcionados, podemos crear otra columna encargada de contener un ts_vector de todos los atributos relacionados con consultas textuales en cada una de las tablas.
```sql
-- Creando los ts_vectors

-- 1. Spotify Inglés
ALTER TABLE spotify_en ADD COLUMN content_idx tsvector;

UPDATE spotify_en
SET content_idx = 
to_tsvector('english',
			CONCAT(track_name, ' ',
				   COALESCE(track_artist,''), ' ',
				   COALESCE(lyrics,''), ' ',
				   COALESCE(track_album_name,''), ' ',
				   COALESCE(track_album_release_date,''), ' ',
				   COALESCE(playlist_name,'') , ' ',
				   COALESCE(playlist_genre,''), ' ',
				   COALESCE(playlist_subgenre,''), ' ',
				   COALESCE(language, '')));
				   
-- 2. Spotify Español
ALTER TABLE spotify_es ADD COLUMN content_idx tsvector;

UPDATE spotify_es
SET content_idx = 
to_tsvector('spanish',
			CONCAT(track_name, ' ',
				   COALESCE(track_artist,''), ' ',
				   COALESCE(lyrics,''), ' ',
				   COALESCE(track_album_name,''), ' ',
				   COALESCE(track_album_release_date,''), ' ',
				   COALESCE(playlist_name,'') , ' ',
				   COALESCE(playlist_genre,''), ' ',
				   COALESCE(playlist_subgenre,''), ' ',
				   COALESCE(language, '')));
```
Para optimizar las consultas, PostgreSQL nos proporciona dos índices para acelerar las búsquedas de texto: GiST y GIN. Existe una ligera diferencia entre estas dos. Según la `documentación de PostgreSQL`, el índice GiST puede producir coincidencias falsas por lo que requiere una verificación extra. En cambio, el índice GIN no genera pérdidas a cambio de un rendimiento dependiente logarítmicamente del número de palabras únicas. Sin embargo, este último solamente almacena los lexemas pertenecientes al `ts_vector`, requiriendo verificar nuevamente las filas para obtener los pesos de cada palabra. A partir de estas definiciones, decidimos utilizar el índice GIN ya que necesitamos la mayor precisión al momento de ejecutar las consultas.
```sql
-- Aplicando el ginIdx
DROP INDEX IF EXISTS idxGinEn;
CREATE INDEX idxGinEn ON spotify_en USING gin(content_idx);

DROP INDEX IF EXISTS idxGinEs;
CREATE INDEX idxGinEs ON spotify_es USING gin(content_idx);
```

# Fuentes
Andrés Moya. (7 de agosto de 2012). *¿Cómo usar búsqueda de texto en PostgreSQL?*. Kaleidos. https://blog.kaleidos.net/como-usar-busqueda-de-texto-en-postgresql/

PostgreSQL. (s.f.). *PostgreSQL: Documentation: 16: 8.11. Text Search Types*. Recuperado el día 7 de noviembre de 2023 de https://www.postgresql.org/docs/current/datatype-textsearch.html

PostgreSQL. (s.f.). *PostgreSQL: Documentation: 16: 12.9. Preferred Index Types for Text Search*. Recuperado el día 7 de noviembre de 2023 de https://www.postgresql.org/docs/current/textsearch-indexes.html