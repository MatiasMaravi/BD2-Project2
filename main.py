from src.classes.InvertIndex import InvertIndex
from app import get_db,close_db
import time

textos = ["books/libro1.txt","books/libro2.txt","books/libro3.txt","books/libro4.txt","books/libro5.txt","books/libro6.txt"]
A1 = InvertIndex("indice_invertido.json")
A1.building(textos)

valores = A1.retrieval("Frodo viaja a obtener los anillos", 6)
print(valores)

def mostrar():
    return valores



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

