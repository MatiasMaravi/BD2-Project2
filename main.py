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
