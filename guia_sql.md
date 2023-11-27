# Creando Base de Datos en PostgreSQL

Para este proyecto, hemos utilizado una tabla auxiliar llamada **spotify_songs**:
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
```

Después de esto, debemos poblar la base de datos con el archivo **new_spotify_songs.csv**:
```sql
COPY spotify_songs(
    track_id,track_name, track_artist, 
	lyrics,track_popularity, track_album_id,
	track_album_name, track_album_release_date,
	playlist_name,playlist_id,playlist_genre,
    playlist_subgenre,danceability,energy,key,loudness,
	mode,speechiness,acousticness,instrumentalness,
	liveness,valence,tempo,duration_ms,language
	)
FROM 'TU_RUTA' DELIMITER ',' CSV HEADER;
```

Hemos observado que tenemos dos idiomas predominantes: inglés y español. Por lo tanto, hemos decidido crear dos tablas que contengan las canciones que cumplan los requisitos:
```sql
DROP TABLE IF EXISTS spotify_en;

CREATE TABLE spotify_en AS
SELECT * FROM spotify_songs
WHERE language = 'en';

DROP TABLE IF EXISTS spotify_es;

CREATE TABLE spotify_es AS
SELECT * FROM spotify_songs
WHERE language = 'es';
```

Ahora, creamos una columna que contenga el **ts_vector** con los respectivos idiomas para cada uno. Luego traspasamos los datos de la tabla auxiliar a las dos tablas creadas:
```sql
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

Para que las consultas sean óptimas, es necesario agregar un índice **GIN** a la última columna agregada:
```sql
DROP INDEX IF EXISTS idxGinEn;
CREATE INDEX idxGinEn ON spotify_en USING gin(content_idx);

DROP INDEX IF EXISTS idxGinEs;
CREATE INDEX idxGinEs ON spotify_es USING gin(content_idx);
```

Solamente quedaría probar su funcionamiento. Esto lo podemos realizar mediante las siguientes consultas:
```sql
-- Queries de ejemplo
SELECT track_artist,track_name,ts_rank(content_idx,query) as rank 
	FROM spotify_en, to_tsquery('english', 'Rock & Love') query WHERE content_idx
	@@ query order by rank desc limit 10;
	
SELECT track_artist,track_name,ts_rank(content_idx,query) as rank 
	FROM spotify_es, to_tsquery('spanish', 'Terror') query WHERE content_idx
	@@ query order by rank desc limit 10;
```