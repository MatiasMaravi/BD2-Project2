import csv

# Ruta del archivo CSV
ruta_archivo = './new_spotify_songs.csv'  # Reemplaza con la ruta de tu archivo CSV

# Variable para almacenar el conteo de filas
conteo_filas = 0

try:
    with open(ruta_archivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # Contamos las filas del archivo CSV
        for row in reader:
            conteo_filas += 1

    print(f"El archivo CSV tiene {conteo_filas} filas.")
except FileNotFoundError:
    print("El archivo no se encontró o la ruta es incorrecta.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
