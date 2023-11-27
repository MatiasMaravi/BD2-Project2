
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


def realizar_consulta(idioma,consulta,topk):
    import os
    if not os.path.exists("blocks_" + idioma):
        print("No existe el indice invertido, por favor cree el indice primero")
        return

    resultado = retrieval(consulta, topk, "blocks_" + idioma, "idf_" + idioma, "norma_" + idioma, idioma)
    print(resultado)
    return resultado
















