import faiss
import numpy as np

def euclidean_distance(x, y):
    return np.sum((x - y) ** 2)

def cosine_distance(x, y):
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

# Tu conjunto de vectores
vectors = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0],
    [10.0, 11.0, 12.0]
], dtype=np.float32)

# Configuración del índice (puedes elegir diferentes algoritmos según tus necesidades)
# index = faiss.IndexFlatL2(len(vectors[0]))  # Índice plano con distancia euclidiana L2

# Configuración del índice HNSWFlat
# dimensionality = len(vectors[0])  # Dimensión de los vectores
# index = faiss.IndexHNSWFlat(dimensionality, 32)  # 32 conexiones por nodo

# FlatL2 y HNSWFlat dan el mismo resultado ya que usan la misma distancia euclidiana L2

# Configuración del índice LSH - Hashing Sensible a la Localidad
# nbits = 16  # Número de bits en la función de hash
# index = faiss.IndexLSH(len(vectors[0]), nbits)

# Configuración del índice FlatIP - Producto Interno
dimensionality = len(vectors[0])  # Dimensión de los vectores
index = faiss.IndexFlatIP(dimensionality)

# Normalizar los vectores
faiss.normalize_L2(vectors)

# Entrenar el índice IVF
index.train(vectors)

# Añadir vectores al índice
index.add(vectors)

# Vector de consulta
query_vector = np.array([2.0, 3.0, 4.0], dtype=np.float32)  # El vector para el cual deseas encontrar vecinos cercanos

# Normalizar el vector de consulta
query_vector /= np.linalg.norm(query_vector)

# Número de vecinos que deseas recuperar
k = 2

# Realizar la búsqueda
distances, indices = index.search(np.array([query_vector], dtype=np.float32), k)

# Imprimir resultados
print(f"Vecinos más cercanos para el vector de consulta:")
print(f"Índices: {indices[0]}")
print(f"Distancias: {distances[0]}")

print("\nDistancia euclidiana entre los vectores de consulta y los vecinos más cercanos:")
print(euclidean_distance(vectors[0], query_vector))
print(euclidean_distance(vectors[1], query_vector))

print("\nDistancia coseno entre los vectores de consulta y los vecinos más cercanos:")
print(cosine_distance(vectors[0], query_vector))
print(cosine_distance(vectors[1], query_vector))