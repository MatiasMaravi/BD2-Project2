# Instalacion de MongoDB en Macos

Homebrew requiere las herramientas de línea de comandos Xcode de Xcode de Apple.
Requisitos:
* Instalar xcode
```
xcode-select --install
```
* Instalar homebrew
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Para descargar la fórmula oficial de Homebrew para MongoDB y las herramientas de base de datos, ejecutando el siguiente comando en su terminal macOS:
```
brew tap mongodb/brew
```

* Actualizar homebrew
```
brew update
```

* Instalar mongodb
```
brew install mongodb-community@7.0
```

Para ejecutar MongoDB realizar lo siguiente
```
brew services start mongodb-community@7.0
```
y luego iniciamos.
```
mongosh
```
# Creamos nuestra base de datos

Realizamos el comando:

```
use BasedeDatosProyect2
```

Creamos nuestra coleccion:

```
db.createCollection("spotify_songs")
```
Insertamos los valores a nuestra coleccion con la siguiente idea de inserccion sera realizada ya que mongodb es un abase de datos no relacional.

```
db.spotify_songs.insert({
    track_id: "some_track_id",
    track_name: "Some Track Name",
    track_artist: "Some Artist",
    lyrics: "Lyrics go here",
    track_popularity: 0.0,
    track_album_id: "some_album_id",
    track_album_name: "Some Album Name",
    track_album_release_date: "Release Date",
    playlist_name: "Some Playlist Name",
    playlist_id: "some_playlist_id",
    playlist_genre: "Genre",
    playlist_subgenre: "Subgenre",
    danceability: 0.0,
    energy: 0.0,
    key: 0.0,
    loudness: 0.0,
    mode: 0.0,
    speechiness: 0.0,
    acousticness: 0.0,
    instrumentalness: 0.0,
    liveness: 0.0,
    valence: 0.0,
    tempo: 0.0,
    duration_ms: 0.0,
    language: "Language"
})
```
Para popular y llenar nuestra base de datos y coleccion con la informacion del csv haremos lo siguiente con el comando:

```
mongoimport --db BasedeDatosProyect2 --collection spotify_songs --type csv --headerline --file /ruta_al_archivo/spotify_songs.csv
```

# Indexacion en MongoDB

MongoBD para la recuperacion de informacion, utiliza un indice especializado en campos de tipo texto, a este se le conoce como `indice de texto`.

Este indice permite realizar busquedas en campos que sean cadenas o un array de elementos de cadena, actualmente existen tres versiones de este eficiente metodo de indexacion:

## Idioma por defecto
El idioma por defecto a usar es el ingles, este selecciona y determina las reglas que se utilizan para analizar las raices de las palabras (sufijo-tallo) y define las palabras de parada que se filtran. Por ejemplo, en inglés, las raíces sufijales incluyen -ing y -ed, y las palabras de parada incluyen the y a. 

## Sustitución de idioma
Especifique un nombre de campo diferente para sustituir el campo de idioma.

## Pesos de campo
Este metodo utiliza una tecnica llamada `inverted index` o `indice invertido`, MongoDB multiplica el número de coincidencias por el peso y suma los resultados. MongoDB utiliza esta suma para calcular la puntuación del documento. Seleccione un campo de la lista, especifique su peso en la casilla y haga clic en Añadir campo. El peso de campo por defecto es 1.(Esta es la version predeterminada)


## Indice invertido

El indice invetido en MongoDB, funciona de la siguiente manera:

1. Se tokeniza el texto, es decir, se separa en palabras.
2. Se eliminan las palabras vacias, como articulos, preposiciones, etc.
3. Cada token se almacena en el indice, junto con una referencia del documento en el que aparece.
4. Se calcula el peso de cada token en cada documento, y se almacena en el indice.
5. Para realizar una consulta de texto completo se utiliza el operador `$text`, que recibe como parametro la consulta, y devuelve los documentos que contienen las palabras de la consulta, ordenados por relevancia.
6. MongoDB utiliza el algoritmo `TF-IDF` para calcular la relevancia de cada documento.

  ### Ejemplo de uso

 - Creamos un índice de texto en un campo llamado "descripcion" en una colección  llamada "productos":
  ```python
    db.productos.createIndex({ descripcion: "text" });
  ```
  - Para realizar una consulta de texto completo, utilizamos el operador `$text`, en este caso, buscamos los documentos que contienen la palabra "pantalon" en el campo "descripcion":
  ```python
    db.productos.find({ $text: { $search: "pantalon" } });
  ```

En nuestra base dedatos actualizamos la coleccion spotify_songs de cada inserccion con el comando:

```
db.spotify_songs.updateMany({}, { $set: { content_idx: '' } })
```
Haremos un update a los valores insertados que tenian inicialmente valores nulos, pero ahora con lo que se indica:
```
db.spotify_songs.find().forEach(function(doc) {
    const content_idx = [doc.track_name, doc.track_artist, doc.lyrics, doc.track_album_name, doc.track_album_release_date, doc.playlist_name, doc.playlist_genre, doc.playlist_subgenre, doc.language].filter(Boolean).join(' ');
    db.spotify_songs.update({ _id: doc._id }, { $set: { content_idx: content_idx } });
});
```

Creamos el indice de en el value agregado:
```
db.spotify_songs.createIndex({ content_idx: 'text' }, { default_language: 'en', language_override: 'en' })
```

Verificamos que el indice fue creado
```
db.spotify_songs.getIndexes()
```

Consultas:

```
db.spotify_songs.find(
   { $text: { $search: "Holy" } },
   { score: { $meta: "textScore" }, track_name: 1 }
).sort({ score: { $meta: "textScore" } }).limit(10)


db.spotify_songs.find(
   { $text: { $search: "Paranoid" } },
   { score: { $meta: "textScore" }, track_name: 1, track_artist: 1 }
).sort({ score: { $meta: "textScore" } }).limit(1000)

```

Controlando el tiempo en consultas:


```
var startTime = new Date();

db.spotify_songs.find(
   { $text: { $search: "Paranoid" } },
   { score: { $meta: "textScore" }, track_name: 1, track_artist: 1 }
).sort({ score: { $meta: "textScore" } }).limit(64000)

var endTime = new Date();

var executionTime = endTime - startTime;

print("Tiempo de ejecución: " + executionTime + " ms");

```
<img width="1440" alt="Captura de pantalla 2023-11-04 a la(s) 00 43 24" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/615359ad-5100-4f09-9be9-d18fb4011afd">

<img width="1440" alt="Captura de pantalla 2023-11-04 a la(s) 00 43 56" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/d82728cb-6cd2-4436-b800-736adad89a75">

**Con N=1000, Tiempo de ejecución es 63 ms.**


<img width="1440" alt="Captura de pantalla 2023-11-04 a la(s) 00 45 02" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/ed85741e-75fd-4233-810a-b9b6e683ea55">

<img width="1436" alt="Captura de pantalla 2023-11-04 a la(s) 00 45 34" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/1e94e16b-7a10-4d84-8bc2-139bbb2c5dd3">

**Con N=2000, Tiempo de ejecución es 62 ms.**

<img width="1440" alt="Captura de pantalla 2023-11-04 a la(s) 00 50 52" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/14e228cc-5c3b-4655-8174-1e0f181b71ce">

<img width="1440" alt="Captura de pantalla 2023-11-04 a la(s) 00 51 06" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/2a94cce2-bd16-4a9d-a442-5c8cb76d4f60">

**Con N=4000, Tiempo de ejecución es 74 ms.**

<img width="1440" alt="Captura de pantalla 2023-11-04 a la(s) 00 52 01" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/585d8484-cb25-4021-912c-2630d93ef448">

<img width="1440" alt="Captura de pantalla 2023-11-04 a la(s) 00 53 27" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/7fa239cc-2286-4bee-8076-adf2e42ac206">

**Con N=8000, Tiempo de ejecución es 67 ms.**

<img width="1432" alt="Captura de pantalla 2023-11-04 a la(s) 00 56 04" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/2e99217d-27d6-48af-b97e-cc54fc2accb5">

<img width="1440" alt="Captura de pantalla 2023-11-04 a la(s) 00 55 45" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/6779954b-9239-46ce-bbf6-80e9d993f47e">

**Con N=16000, Tiempo de ejecución es 57 ms.**

<img width="1440" alt="Captura de pantalla 2023-11-04 a la(s) 00 57 27" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/0dd794bb-c464-4615-96d4-7ff5cea3f43d">

<img width="1439" alt="Captura de pantalla 2023-11-04 a la(s) 00 57 12" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/dcf8c685-0942-4342-8cb7-56fa33dfb3e1">

**Con N=32000, Tiempo de ejecución es 62 ms.**

<img width="1440" alt="Captura de pantalla 2023-11-04 a la(s) 01 00 12" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/2de2aa85-e05d-477e-9ae0-259cdf68369b">

<img width="1440" alt="Captura de pantalla 2023-11-04 a la(s) 01 00 24" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/78ef4f55-6614-404e-bd52-90b6021f5ee4">

**Con N=64000, Tiempo de ejecución es 65 ms.**



