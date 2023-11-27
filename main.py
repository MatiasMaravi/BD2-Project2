<<<<<<< HEAD
from app import app
import psycopg2
from flask import g
import time
=======
>>>>>>> main
from src.classes.SPIMI import BSBI
from src.utils.building import building, retrieval
import time
import sys
<<<<<<< HEAD
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
    Indice = BSBI(size_block=40960,archivo="new_spotify_songs.csv",funcion_sizeof=sys.getsizeof)
    Indice.SPIMI()
    Indice.merge_index()
    building()
    tiempo_final = time.time()
    print("indice creado en: ",tiempo_final-tiempo_inicial," segundos")


def realizar_consulta(idioma,consulta,topk):
    import os
    if not os.path.exists("blocks_" + idioma):
        print("No existe el indice invertido, por favor cree el indice primero")
        return

    resultado = retrieval(consulta, topk, "blocks_" + idioma, "idf_" + idioma, "norma_" + idioma, idioma)
    print(resultado)
    return resultado

def run_query(query):
    start_time = time.time()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time
=======

def crear_indice(idioma):
    tiempo_inicial = time.time()
    Indice = BSBI(size_block=40960,archivo="spotify_songs_"+idioma+".csv",funcion_sizeof=sys.getsizeof,carpeta="blocks_"+idioma)
    Indice.SPIMI(idioma=idioma)
    Indice.merge_index()
    building(archivo = "spotify_songs_"+idioma+".csv",carpeta="blocks_"+idioma,idfname="idf_"+idioma,normaname="norma_"+idioma)
    tiempo_final = time.time()
    print("indice creado en: ",tiempo_final-tiempo_inicial," segundos")

def realizar_consulta(idioma):
    import os
    if not os.path.exists("blocks_"+idioma):
        print("No existe el indice invertido, por favor cree el indice primero")
        return
    consulta = input("Ingrese la consulta: ")
    k = int(input("Ingrese el numero de resultados: "))
    resultado = retrieval(consulta,k,"blocks_"+idioma,"idf_"+idioma,"norma_"+idioma,idioma)
    print(resultado)

def seleccionar_idioma():
    print("1. Español")
    print("2. Ingles")
    idioma = input("Ingrese el idioma: ")
    if idioma == "1":
        return "es"
    elif idioma == "2":
        return "en"
    else:
        print("Idioma no soportado")
        return seleccionar_idioma()

def menu():
    idioma = seleccionar_idioma()
    print("1. Crear Indice Invertido")
    print("2. Realizar Consulta")
    print("3. Salir")
    opcion = int(input("Ingrese una opcion: "))
    if opcion == 1:
        crear_indice(idioma)
        input("Presione enter para continuar")
        menu()
    elif opcion == 2:
        realizar_consulta(idioma)
        input("Presione enter para continuar")
        menu()
    elif opcion == 3:
        print("Adios")
        
if __name__ == "__main__":
    menu()
>>>>>>> main
