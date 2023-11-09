# BD2-Project2 🔍
## 📝 Descripción del Proyecto
El siguiente proyecto trata sobre entender y aplicar los algoritmos de
búsqueda y recuperación de la información basado en el contenido. 
## 🧑‍🤝‍🧑 Integrantes del Equipo

Un equipo diverso y apasionado de estudiantes está detrás de este proyecto, listo para sumergirse en el reino de las búsquedas y de la indexación multidimensional. Permítanos presentarnos:

| Nombre Completo                     | Usuario Github   |
|-------------------------------------|------------------|
| Matias Fabricio Maravi Anyosa       | MatiasMaravi     |
| Leonardo Daniel Salazar Isidro      | LeoIsidro        |
| Jerimy Pierre Sandoval Rivera       | Jerimy2021       |
| Alejandro Gerardo Calizaya Alvarez  | AlejandroCalizaya|
| Jose Leandro Machaca Soloaga        | JLeandroJM       |
## 📂 Estructura del Repositorio

- 📁 `assets`: En esta carpeta se encuentran los archivos estáticos del proyecto.
- | 📁 `docs`: En esta carpeta se encuentran los documentos de texto que explican el proyecto.
- | 📁 `images`: En esta carpeta se encuentran las imágenes que se usan en el proyecto.
- | 📁 `resources`: En esta carpeta se encuentran los archivos auxiliares del proyecto.
- 📁 `books`: En esta carpeta se encuentran los libros que se usan en el proyecto para realizar las consultas.
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

## Ejemplo de uso
Ejecutar el siguiente comando en la terminal:
```bash
python3 main.py
```
Después de ejecutar el comando se mostrará un menú donde podrás realizar la consulta textual sobre la tabla de canciones de spotify.
También habrá la opción para crear el índice invertido (guardado en blocks_index) si aún no fue creado.
## Experimento
|   | PostgreSQL |
| ------------- | ------------- |
| N = 1000  | 14.778 ms  |
| N = 2000  | 15.129 ms  | 
| N = 4000  | 15.072 ms  | 
| N = 8000  | 14.142 ms  | 
| N = 16000  | 27.289 ms  | 