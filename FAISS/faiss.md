# Guía para utilizar la librería FAISS
En esta pequeña guía se hablará de cómo usar, qué índice utilizamos y por qué utilizamos ese índice.

En primer lugar, es necesario comprender que es FAISS. La librería Facebook IA Similarity Search, o por sus siglas FAISS, es una librería creada por Meta para optimizar la búsqueda de similitudes y agrupaciones de vectores densos, es decir, esos vectores de cualquier tamaño, hasta aquellos que no quepan en RAM.

Existen tres métodos de indexación: Flat, HNSW y NSG. El primero es utilizada para búsqueda secuencia por lo que es recomendable usarlo para datos de baja dimensionalidad. Los dos últimos son utilizados para una búsqueda más eficiente y cuando se utilizan datos de mayor dimensionalidad a costa de agregar una estructura de indexación sobre los vectores. Además, existen dos tipos de implementación para esta librería: CPU y GPU. La diferencia entre estas dos es que, como tal vez pueda deducirse, las consultas realizadas en el GPU serán más rápidas siempre y cuando la entrada y la salida se mantengan en este componente.

### Instalación de la librería
Para este proyecto, como la mayoría de integrantes no contamos con una GPU, hemos decidido instalar la versión que utiliza CPU con el siguiente comando:
```bash
pip3 install faiss-cpu
```

Si desea instalar la versión que utiliza GPU, solamente sería el siguiente cambio:
```bash
pip3 install faiss-gpu
```

## Índices del FAISS

Esta librería cuenta con 10 índices:
1) IndexFlatL2
2) IndexFlatIP
3) IndexHNSWFlat
4) IndexIVFFlat
5) IndexLSH
6) IndexScalarQuantizer
7) IndexPQ
8) IndexIVFScalarQuantizer
9) IndexIVFPQ
10) IndexIVFPQR

Cada índice tiene un propósito diferente que se podrá leer en está documentación: https://github.com/facebookresearch/faiss/wiki/Faiss-indexes.

Sin embargo, para este proyecto, es necesario utilizar aquellos índices que puedan soportar un gran tamaño de datos con alta dimensionalidad. Es por eso que utilizamos el índice **IndexHNSWFlat**.

Si bien existen otros índices que soportan los requerimientos mencionados antes, hemos comprobado que este índice nos rinde mejor al momento de retornarnos un resultado. Como se puede observar en su nombre, este índice hace uso de dos métodos de indexación: HNSW y Flat. Esto con el fin de simplificar las búsquedas planas del Flat mediante HNSW. Además, obtuvimos respuestas más rápidas que los anteriores índices teniendo en cuenta la similitud de los vectores que requerimos.

Cabe resaltar que, en este caso, los resultados de la similitud de audios estamos comprobando que tan parecido es la progresión musical en comparación a la query. Por lo tanto, no tenemos en cuenta lo que sería el género de las canciones.

# Fuentes
- Meta. (s.f.) *GitHub - facebookresearch/faiss: A library for efficient similarity search and clustering of dense vectors*. Github. Recuperado el 25 de noviembre de 2023 de https://github.com/facebookresearch/faiss

- Meta. (s.f.) *Faiss indexes · facebookresearch/faiss Wiki · GitHub*. Github. Recuperado el 25 de noviembre de 2023 de https://github.com/facebookresearch/faiss/wiki/Faiss-indexes
