import os
import json
import math
import numpy as np
import pandas as pd
from .preprocesamiento import preprocesamiento
def calculate_tf(carpeta):
    index_temp = {}

    for nombre_archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, "r") as f:
                index_temp = json.load(f)
                for key in index_temp:
                    index_temp[key] = {k: math.log10(1 + v) for k, v in index_temp[key].items()}

            with open(ruta_archivo, "w") as f:
                json.dump(index_temp, f,ensure_ascii=False, indent=4)

    print("TF calculado")
    
def calculate_idf(carpeta,num_books):
    # IDF

    # Cargamos el indice invertido global por bloques

    df={}

    for nombre_archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, "r") as f:
                index_temp = json.load(f)
                for key in index_temp:
                    df[key] = len(index_temp[key])


    # Calculamos el idf

    div = math.log10(num_books)

    for token in df:
        df[token] = div - math.log10(df[token])

    # Guardamos el idf en un archivo
    with open("data/idf.json", "w") as f:
        json.dump(df, f,ensure_ascii=False, indent=4)

    print("IDF calculado")
    return df
    
def calculate_norma(carpeta,df,books):
    # Calculamos la norma
    # Cargamos el indice invertido global por bloques
    # Cargamos el idf
    norma = {}
    for nombre_archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, "r") as f:
                index_temp = json.load(f)
                for key in index_temp:
                    for book in index_temp[key]:
                        if book in norma:
                            norma[book].append(index_temp[key][book]*df[key])
                        else:
                            norma[book] = [index_temp[key][book]*df[key]]

    for key in norma:
        if len(norma[key])<len(books):
            norma[key].extend([0]*(len(books)-len(norma[key])))

    for key in norma:
        norma[key] = np.linalg.norm(np.array(norma[key]))        


    # Guardamos la norma en un archivo

    with open("data/norma.json", "w") as f:
        json.dump(norma, f,ensure_ascii=False, indent=4)

    print("Norma calculada")

def validate_query(query_term_unic,idf) -> set:
    aux = set()
    for term in query_term_unic:
    # Validamos si existe el término en nuestros diccionarios
        if term in idf:
            aux.add(term)
    return aux

def building():
    dataframe = pd.read_csv("spotify_songs.csv")
    calculate_tf("blocks_index")
    df = calculate_idf("blocks_index",dataframe.shape[0])
    calculate_norma("blocks_index",df,dataframe["track_id"].tolist())

def retrieval(query, k) -> list:
    queryPrep = preprocesamiento(query)
    query_term_unic=set(queryPrep)

    # Cargamos el idf y la norma

    with open("data/idf.json", "r") as f:
        idf = json.load(f)

    with open("data/norma.json", "r") as f:
        norma = json.load(f)     

    score = {}

    for key in norma.keys():
        score[key] = 0

    # Validamos si existe el termino en nuestros diccionarios
    query_term_unic=validate_query(query_term_unic,idf)

    if(len(query_term_unic)==0):
        return score

    lenght_query=[]

    for term in query_term_unic:
        # calcular el tf-idf del query
        term_tf = math.log10(1+queryPrep.count(term))
        term_idf = idf[term]

        # Buscar el termino en el indice invertido global

        for nombre_archivo in os.listdir("blocks_index"):
            ruta_archivo = os.path.join("blocks_index", nombre_archivo)
            if os.path.isfile(ruta_archivo):
                with open(ruta_archivo, "r") as f:
                    index = json.load(f)
                    if term in index:
                        break

        term_doc = index[term]

        lenght_query.append(term_tf*term_idf)

        for doc in term_doc:
            w_td = index[term][doc]*term_idf
            w_tq = term_tf*term_idf
            score[doc] += w_td * w_tq

    norma_query=np.linalg.norm(np.array(lenght_query))

    for doc in score:
        score[doc] /= (norma[doc] * norma_query)
        score[doc] = round(score[doc], 2)

    result = sorted(score.items(), key=lambda x: x[1], reverse=True)

    return result[:k]

