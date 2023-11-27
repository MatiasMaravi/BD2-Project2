import math
import numpy as np
from collections import defaultdict
def tf_dic(tf) -> dict:
    for token, books in tf.items():
        for book, freq in books.items():
            books[book] = math.log10(1 + freq)
    return tf

def idf_dic(df, num_textos) -> dict:
    div = math.log10(num_textos)
    for token in df:
        df[token] = div - math.log10(df[token])
        # df[token] = math.log10(num_textos / df[token])
    return df

def tf(books, textos) -> dict:
    frecuencia = defaultdict(lambda: defaultdict(int))

    for i, libro in enumerate(books):
        for token in libro:
            frecuencia[token][textos[i]] += 1
    
    return dict(frecuencia)

def df(books) -> dict:
    pesos = defaultdict(int)

    for libro in books:
        for token in set(libro):
            pesos[token] += 1

    return dict(pesos)


# La norma se saca a partir de los pesos tf-idf
def norma(tf, idf, collection_text) -> dict:
    length = {}

    TF_IDF = np.array([[tf[token][book] * idf[token] for token in tf] for book in collection_text])

    for i, book in enumerate(collection_text):
        length[book] = np.linalg.norm(TF_IDF[i])

    return length