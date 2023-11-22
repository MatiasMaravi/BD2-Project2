import psycopg2
from psycopg2.extras import Json
import pandas as pd

# Conexión a la base de datos
conexion = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="40101109"
)

def crear_tabla():
    # Crear un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    # Crear la tabla
    cursor.execute("DROP TABLE IF EXISTS Ropa")
    cursor.execute("CREATE TABLE Ropa (id varchar PRIMARY KEY, vector_caracteristico cube)")

    # Confirmar los cambios en la base de datos
    conexion.commit()

    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()


def insertar_datos():
    # Crear un cursor para ejecutar comandos SQL
    cursor = conexion.cursor()

    df = pd.read_csv("features.csv")

    for i in range(1,len(df)):
        lista=[]
        for j in range(1,len(df.columns)):
            lista.append(df.iloc[i,j])

        # Convertir el array a una cadena en formato adecuado para un cubo en PostgreSQL
        vector_str = f"({', '.join(map(str, lista))})"

        # Utilizar el tipo de vector de PostgreSQL para insertar el cubo
        consulta = "INSERT INTO Ropa (id, vector_caracteristico) VALUES (%s, %s)"
        cursor.execute(consulta, (df.iloc[i,0], vector_str))

        # Confirmar los cambios en la base de datos
        conexion.commit()

    consulta = "CREATE INDEX vector_caracteristico_idx ON Ropa USING gist(vector_caracteristico)"
    cursor.execute(consulta)

    print("Se han insertado los datos correctamente")

    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()

def consulta_similar(track_id,k):
    cursor = conexion.cursor()

    consulta = "SELECT vector_caracteristico FROM Ropa WHERE id = %s"
    cursor.execute(consulta, (track_id,))
    vector = cursor.fetchone()[0]

    # Realizar la consulta
    consulta = "SELECT id, cube_distance(vector_caracteristico, %s) AS distancia FROM Ropa ORDER BY vector_caracteristico <-> %s LIMIT %s"
    cursor.execute(consulta, (vector, vector, k))

    # Obtener los resultados
    resultados = cursor.fetchall()

    diccionario = []

    for resultado in resultados:
        diccionario.append({"track_id":resultado[0]})

    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()

    return diccionario

#crear_tabla()
#insertar_datos()

print(consulta_similar("0a4agFmqHXxcZl1nho1BxM",10))