from pydub import AudioSegment
import os
import librosa
import numpy as np
import csv
import pandas as pd

from sklearn.preprocessing import StandardScaler


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


def save_features_to_csv(file_path, output_csv):
    # Obtener la lista de archivos en la carpeta
    track_id = os.path.split(file_path)[1][:-4]

    with open(output_csv, 'a', newline='') as csvfile:
        # Definir los nombres de las columnas
        print(f"Procesando {track_id}...")
        features = extract_features(file_path)
        fieldnames = ['track_id'] + [f'f{i}' for i in range(1, 1 + len(features))]
        
        # Inicializar el escritor CSV
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Escribir la fila en el CSV
        writer.writerow({'track_id': track_id, **{f'f{i}': feature for i, feature in enumerate(features, start=1)}})

# saber canciones que falta procesar
def extraer_caracteristicas(archivo):
    # Carpeta de entrada con archivos .mp3
    carpeta_entrada = "music"

    # Carpeta de salida para los archivos .wav
    carpeta_salida = "music_wavs"
    salida = "new_featurespepe.csv"

    # Asegúrate de que la carpeta de salida exista
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)


    # Construir las rutas de entrada y salida
    ruta_entrada = os.path.join(carpeta_entrada, archivo)
    nombre_archivo = os.path.splitext(archivo)[0]  # Obtener el nombre del archivo sin extensión
    ruta_salida = os.path.join(carpeta_salida, f"{nombre_archivo}.wav")

    # Cargar el archivo .mp3 y guardarlo como .wav
    audio = AudioSegment.from_mp3(ruta_entrada)
    audio.export(ruta_salida, format="wav")
    save_features_to_csv(ruta_salida, salida)
    os.remove(ruta_salida)


carpeta = "music"
salida = "new_featurespepe.csv"
max_len = 360
if not os.path.exists(salida):
    with open(salida, 'w', newline='') as csvfile:
        # Definir los nombres de las columnas
        fieldnames = ['track_id'] + [f'f{i}' for i in range(1, 1 + max_len)]

        # Inicializar el escritor CSV
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Escribir la fila en el CSV
        writer.writeheader()
df = pd.read_csv(salida)

for archivo in os.listdir(carpeta):
    track_id = os.path.split(archivo)[1][:-4]
    if track_id not in df['track_id'].values:
        extraer_caracteristicas(archivo)
    break
