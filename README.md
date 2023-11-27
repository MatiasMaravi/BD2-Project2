# BD2-Project2 🔍
## 📝 Descripción del Proyecto
El siguiente proyecto trata sobre entender y aplicar los algoritmos de
búsqueda y recuperación de la información basado en el contenido. 
## 🧑‍🤝‍🧑 Integrantes del Equipo

Un equipo diverso y apasionado de estudiantes está detrás de este proyecto, listo para sumergirse en el reino de las búsquedas y de la indexación multidimensional. Permítanos presentarnos:

|    Matias Maravi    |    Leandro Machaca    |    Leonardo Isidro    |    Alejandro Calizaya    | Jerimy Sandoval |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| ![](https://avatars.githubusercontent.com/u/91230547?v=4) | ![](https://avatars.githubusercontent.com/u/102132128?s=400&v=4) | ![](https://avatars.githubusercontent.com/u/90939274?v=4) | ![](https://avatars.githubusercontent.com/u/91271621?v=4) | ![](https://avatars.githubusercontent.com/u/91238497?v=4) |
| [github.com/MatiasMaravi](https://github.com/MatiasMaravi) | [github.com/JLeandroJM](https://github.com/JLeandroJM) | [github.com/LeoIsidro](https://github.com/LeoIsidro) | [github.com/AlejandroCalizaya](https://github.com/AlejandroCalizaya)| [github.com/Jerimy2021](https://github.com/Jerimy2021) |


## 📂 Estructura del Repositorio
- 📁 `app`: En esta carpeta se encuentran los archivos necesarios para ejecutar el proyecto en web.
- 📁 `archive`: En esta carpeta se encuentran algunos archivos que ya no se usan en el proyecto.
- 📁 `assets`: En esta carpeta se encuentran los archivos estáticos del proyecto.
- | 📁 `docs`: En esta carpeta se encuentran los documentos de texto que explican el proyecto.
- | 📁 `images`: En esta carpeta se encuentran las imágenes que se usan en el proyecto.
- | 📁 `resources`: En esta carpeta se encuentran los archivos auxiliares del proyecto.
- 📁 `FAISS`: En esta carpeta se encuentra nuestra experimentación del índice multidimensional FAISS.
- 📁 `knn`: En esta carpeta se encuentra nuestra experimentación del algoritmo KNN.
- 📁 `src`: En esta carpeta esta todo nuesto código fuente
- |📁 `classes`: En esta carpeta se encuentran todas las clases que definimos para nuestro proyecto
- |📁 `utils`: En esta carpeta se encuentran todas las funciones auxiliares necesarias para el proyecto
- 📄 `README.md`: ¡Estás aquí! Este archivo contiene la información esencial que necesitas para comprender el proyecto.

## 🚀 Objetivos del Proyecto
El proyecto se divide en dos
partes: 
1. **Construcción eficiente de un Índice  Invertido** para tareas de búsqueda y recuperación en
documentos de texto.
2. **Construcción de una estructura multidimensional** para dar soporte a las
búsqueda y recuperación eficiente de imágenes / audio usando vectores característicos. 
Ambas implementaciones serán aplicadas para mejorar la búsqueda en un sistema de recomendación.
## Descripción del dominio de datos
Para probar la similitud de nuestro proyecto hacemos uso de un dataset de músicas de 
[Spotify](https://www.kaggle.com/datasets/imuhammad/audio-features-and-lyrics-of-spotify-songs). Este dataset contiene 15 mil canciones de Spotify, cada canción tiene los siguientes atributos:
- `track_id`: Song ID
- `track_name`: Nombre de la música
- `track_artist`: Nombre del artista
- `lyrics`: Letra de la canción
- `track_popularity`: Popularidad de la canción
- `track_album_id`: Album ID
- `track_album_name`: Nombre del album
- `track_album_release_date`: Fecha de lanzamiento del album
- `playlist_name`: Nombre de la playlist
- `playlist_id`: Playlist ID
- `playlist_genre`: Género de la playlist
- `playlist_subgenre`: Subgénero de la playlist
- `language`: Idioma de la canción

En total solo eran 18 mil canciones, pero se eliminaron las canciones que no eran de idioma inglés ni español, por ello quedaron 15 mil canciones.

## Importancia de aplicar indexación
Si quisieramos tener una aplicación donde al colocar una query nos muestre las canciones más parecidas a la query, tendríamos que comparar la query con todas las canciones de la base de datos, esto sería muy ineficiente, ya que tendríamos que comparar la query con 15 mil canciones, por ello es necesario aplicar indexación para que la búsqueda sea más eficiente.
El método de indexación que usamos lo hacemos sobre la metadata del dataset de spotify, para ello usamos el algoritmo SPIMI, que nos permite crear un índice invertido, que es una estructura de datos que nos permite buscar palabras en un documento de manera eficiente.

## Ejemplo de uso
Ejecutar el siguiente comando en la terminal:
```bash
python3 main.py
```
Después de ejecutar el comando se mostrará un menú donde podrás realizar la consulta textual sobre la tabla de canciones de spotify.
También habrá la opción para crear el índice invertido (guardado en blocks_index) si aún no fue creado.

## Experimento
|               | PostgreSQL     | MongoDB    | SPIMI      |
| ------------- | -------------- | ---------- | ---------- |
| N = 1000      | 14.778 ms      | 0.116 ms   | 513.140 ms |
| N = 2000      | 15.129 ms      | 0.197 ms   | 477.520 ms |
| N = 4000      | 15.072 ms      | 0.161 ms   | 474.942 ms |
| N = 8000      | 14.142 ms      | 0.204 ms   | 486.690 ms |
| N = 15000     | 27.289 ms      | 0.256 ms   | 462.502 ms |


## Experimento 2
|               | KNN-Secuencial | KNN-RTree  | FAISS      | 
| ------------- | -------------- | ---------- | ---------- |
| N = 1000      | 28.852 ms      | 0.050 ms   | 0.114 ms   | 
| N = 2000      | 59.175 ms      | 0.065 ms   | 0.158 ms   | 
| N = 4000      | 115.341 ms     | 0.072 ms   | 0.123 ms   | 
| N = 8000      | 230.965 ms     | 0.103 ms   | 0.198 ms   | 
| N = 15000     | 444.175 ms     | 0.225 ms   | 0.206 ms   | 

## Análisis y discusión
El índice FAISS es mucho más óptimo en altas dimensiones a diferencias del knn secuencial y el knn con RTree porque está optimizado para trabajar con alta cantidad de datos y una alta dimensionalidad al hacer uso de grafos y trabajar en cpu.


## Wiki
Para más información sobre nuestra implementación, puedes visitar nuestra [Wiki](https://github.com/MatiasMaravi/BD2-Project2/wiki) donde encontrarás más detalles sobre el proyecto.