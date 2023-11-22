
from app import app
import psycopg2
from flask import g
import time
from src.classes.SPIMI import BSBI
from src.utils.building import building, retrieval
import time
import sys
import pandas as pd


app.config['DATABASE_URI'] = 'postgresql://postgres:40101109@localhost/BaseII'



def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(app.config['DATABASE_URI'])
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def run_query(query, consulta_str, topk_int):
    start_time = time.time()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, (consulta_str, topk_int))
    result = cursor.fetchall()
    cursor.close()
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

def crear_indice():
    tiempo_inicial = time.time()
    Indice = BSBI(size_block=40960,archivo="spotify_songs.csv",funcion_sizeof=sys.getsizeof)
    Indice.SPIMI()
    Indice.merge_index()
    building()
    tiempo_final = time.time()
    print("indice creado en: ",tiempo_final-tiempo_inicial," segundos")

def realizar_consulta(consulta,topk):
    import os
    if not os.path.exists("blocks_index"):
        print("No existe el indice invertido, por favor cree el indice primero")
        return


    resultado = retrieval(consulta,topk)
    return resultado

def crear_tabla():
    # Crear un cursor para ejecutar comandos SQL
    conn = get_db()
    cursor = conn.cursor()

    # Crear la tabla
    cursor.execute("DROP TABLE IF EXISTS Ropa")
    cursor.execute("CREATE TABLE Ropa (id varchar PRIMARY KEY, vector_caracteristico cube)")

    conn.commit()
    cursor.close()


def insertar_datos():
    conn = get_db()
    cursor = conn.cursor()

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
        conn.commit()

    consulta = "CREATE INDEX vector_caracteristico_idx ON Ropa USING gist(vector_caracteristico)"
    cursor.execute(consulta)

    print("Se han insertado los datos correctamente")

    # Cerrar el cursor y la conexión
    cursor.close()


def consulta_similar(track_id,k):
    conn = get_db()
    cursor = conn.cursor()

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


    return diccionario







