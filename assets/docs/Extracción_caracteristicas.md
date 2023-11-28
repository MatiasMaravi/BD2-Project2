# Extraccion de caracteristicas de Dataset de Spotify
Para poder comparar la similitud entre las canciones es necesario procesarlas y extraer sus caracteristicas, para ello se utilizo la libreria  "Librosa" que nos permite extraer las caracteristicas de las canciones. Más especificamente usamos la funcion "librosa.feature.chroma_stft" que nos permite extraer la cromatografia de la cancion, que es una representacion de la distribucion de la energia de la frecuencia de la cancion.

# ¿Por qué escogimos estas característica?
La libreria "Librosa" nos brinda diversas funciones para extraer las caracteristicas de las canciones. Algunas nos brindan la intensidad del audio a lo largo del tiempo, otras nos brindan la intensidad de las frecuencias a lo largo del tiempo. Pero para este proyecto nos pareció más importante el tono de todas las notas musicales a lo largo de la canción, por lo que decidimos usar la cromatografia de la cancion, que nos brinda la intensidad de cada nota musical a lo largo de la cancion.
## ¿Qué es la cromatografia?
La cromatografia es una representacion de la distribucion de la energia de la frecuencia de la cancion. La cromatografia es una matriz de 12 filas y n columnas, donde n es la cantidad de frames de la cancion, cada fila representa una nota musical y cada columna representa un frame de la cancion, el valor de cada celda representa la intensidad de la nota musical en el frame de la cancion. La cantidad de columnas es variable porque depende de la duracion de la cancion.
![cromatografia](/assets/images/Figure_1.png)

## ¿Cómo solucionamos el problema de columnas variables?
Primero pensamos en usar PCA pero esto nos generó problemas ya que disminuía demasiado las caracteristicas. Necesitabamos un balance entre una considerable cantidad de caracteristicas para retener buena información. Pero no tantas para evitar el sobreajuste. Por lo que decidimos dividir la matriz en 30 segmentos uniformes y tomar la media de cada segmento. Esto nos devuelve una matriz de 12 filas y 30 columnas, donde cada columna representa un segmento de la cancion y cada fila representa una nota musical.

# Funcion extract_features
``` python
scaler = StandardScaler()
def extract_features(file_path):
    # Cargar el archivo de audio
    y, sr = librosa.load(file_path)

    # Extraer características
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    print(chroma_stft.shape)
    #Estandarizamos
    chroma_stft = scaler.fit_transform(chroma_stft.T)
    chroma_stft = chroma_stft.T
    # Dividir en segmentos uniformes
    num_segments = 30
    segment_len = chroma_stft.shape[1] // num_segments

    # Tomar la media de cada segmento
    chroma_stft_uniform = np.mean(chroma_stft[:, :num_segments * segment_len].reshape(12, -1, segment_len), axis=2)
    # Concatenar todas las características en un solo vector
    features = chroma_stft_uniform.flatten()
    
    return features
```
# Pasos para extraer las caracteristicas
Ahora procederé a explicar detalladamente como es que extraemos las caracteristicas de las canciones:
## Paso 1
Cargamos el archivo de audio con librosa.load, esto nos devuelve un arreglo de numpy con los valores de amplitud de la cancion y la frecuencia de muestreo. Es necesario que el archivo de audio este en formato .wav, por lo que se tuvo que convertir los archivos de audio de spotify a este formato, luego de procesada la cancion se elimina el archivo .wav y se deja el archivo original.

``` python
y, sr = librosa.load(file_path)
```

y: arreglo de numpy con los valores de amplitud de la cancion. Esto nos indica la amplitud de la cancion en cada instante de tiempo.
sr: frecuencia de muestreo. Esto nos indica cuantas muestras se toman por segundo, por lo que si la frecuencia de muestreo es de 22050 Hz, significa que se toman 22050 muestras por segundo.
## Paso 2
Extraemos las caracteristicas de la cancion con librosa.feature.chroma_stft, esta funcion nos devuelve una matriz de numpy de 12 filas y n columnas, donde n es la cantidad de frames de la cancion, cada fila representa una nota musical y cada columna representa un frame de la cancion, el valor de cada celda representa la intensidad de la nota musical en el frame de la cancion. La cantidad de columnas es variable porque depende de la duracion de la cancion. Esto es un problema que mitigamos en el siguiente pasos mas adelante.
``` python
chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
```
## Paso 3
Estandarizamos la matriz de caracteristicas, esto lo hacemos para que las caracteristicas tengan una media de 0 y una desviacion estandar de 1. Estandarizar es una buena practica para que las caracteristicas tengan el mismo peso a la hora de compararlas y ninguna caracteristica tenga mas peso que otra.
``` python
chroma_stft = scaler.fit_transform(chroma_stft.T)
chroma_stft = chroma_stft.T
```
La razón por la que la pasamos la transpuesta es porque la funcion scaler.fit_transform espera una matriz del tipo (n_samples, n_features), donde n_samples es la cantidad de frames de la cancion y n_features es la cantidad de caracteristicas, pero la matriz que tenemos es del tipo (n_features, n_samples), por lo que tenemos que transponerla.
Despues de estandarizarla volvemos a transponerla para que quede en el formato original.

## Paso 4
Realizamos una distribución uniforme. Esto lo hacemos con el fin de que todas las matrices tengan la misma cantidad de columnas sin perder tanta informacion. Para ello dividimos la matriz en 30 segmentos uniformes y tomamos la media de cada segmento. Los segmentos los calculamos de la siguiente manera:
``` python
num_segments = 30
segment_len = chroma_stft.shape[1] // num_segments
# Tomar la media de cada segmento
chroma_stft_uniform = np.mean(chroma_stft[:, :num_segments * segment_len].reshape(12, -1, segment_len), axis=2)
```
Lo que pasa en la ultima linea de cṕodigo es que primero tomamos los primeros 30 * segment_len frames de la cancion, luego los reordenamos en una matriz de 12 filas y -1 columnas, donde -1 significa que numpy calcula automaticamente la cantidad de columnas necesarias para que la matriz tenga 12 filas, y luego tomamos la media de cada columna, esto nos devuelve una matriz de 12 filas y 30 columnas, donde cada columna representa un segmento de la cancion y cada fila representa una nota musical. Cabe recalcar que calculamos la media de las columnas y no la de las filas con "axis=2", porque queremos que cada fila represente una nota musical y no un segmento de la cancion.

## Paso 5
Concatenamos todas las caracteristicas en un solo vector. Esto lo hacemos para que cada cancion tenga la misma cantidad de caracteristicas, independientemente de su duracion. Para ello simplemente concatenamos todas las columnas de la matriz en un solo vector.
``` python
# Concatenar todas las características en un solo vector
features = chroma_stft_uniform.flatten()
```
Entonces al final nos queda un vector del siguiente tipo [a1, a2, a3, ..., c30 , ... , b1 , b2 , b3 , ... , b30 , ... , l1 , l2 , l3 , ... , l30], donde a1, a2, a3, ..., a30 representan la intensidad de la nota musical "a" a lo largo de toda la canción, b1, b2, b3, ..., b30 representan la intensidad de la nota musical "b" a lo largo de toda la cancion, y asi sucesivamente hasta llegar a l30, que representa la intensidad de la nota musical l a lo largo de toda la canción. Esto lo hacemos para que cada cancion tenga la misma cantidad de caracteristicas, independientemente de su duracion. Se puede sobreentender que "1" representa el promedio de esa nota en el segmento "1", lo mismo con el segmento 2  y asi sucesivamente hasta llegar al segmento 30.