import pandas as pd
import numpy as np
import faiss
import time
print("Índice Faiss iniciado")

# Leer archivo CSV
df = pd.read_csv('./FAISS/new_new_features.csv')

# Seleccionar desde la columna 1 hasta la última
songs = df.iloc[:, 1:].values
songs = songs.astype(np.float32)
# print("Songs:\n",songs)

# Configuración del índice HNSWFlat
dimensionality = len(songs[0])  # Dimensión de los vectores
index = faiss.IndexHNSWFlat(dimensionality, 32)  # 32 conexiones por nodo

index.add(songs)

def getSongs(songID: str):
    # Obtener el número de fila de la canción
    numFila = df[df['track_id'] == songID].index[0]

    # Vector de consulta
    query_song = df.iloc[numFila, 1:].values  # El vector para el cual deseas encontrar vecinos cercanos
    query_song = query_song.astype(np.float32)
    # print("Query song:\n",query_song)

    # Número de vecinos que deseas recuperar
    k = 11  # Se escoge 11 porque el primer vecino es la misma canción

    # Tomar el tiempo de inicio
    start = time.time()

    # Realizar la búsqueda
    distances, indices = index.search(np.array([query_song], dtype=np.float32), k)

    # Tomar el tiempo de finalización
    end = time.time()

    # Imprimir el tiempo de ejecución
    print("Tiempo de ejecución: {} seconds".format(end - start))

    # Pasar a lista
    indices = indices[0].tolist()

    # Devolviendo en formato necesario para mostrar en el frontend
    return [{"track_id": song} for song in df.iloc[indices, 0].values[1:]]

# Prueba
# topK = getSongs("51TG9W3y9qyO8BY5RXKgnZ")
# print("Top 10:")
# print(topK)