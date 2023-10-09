import math
import numpy as np
def tf_dic(tf) -> dict:
    #np.log10(1 + np.array([[TF[token]['libro'+ str(i+1)] for token in TF] for i,book in enumerate(collection)]))
    for token in tf:
        for book in tf[token]:
            tf[token][book]=math.log10(1+ tf[token][book])
    return tf
def idf_dic(df,num_textos) -> dict:
    #IDF = np.log10(len(collection)/np.array([DF[token] for token in DF]))
    for token in df:
        df[token]=math.log10(num_textos/df[token])

    return df

def tf(books,textos) -> dict:
    frecuencia = {}
    tokens = []
    #1. Crear una lista de tokens general
    for i in books:
        tokens+=i

    tokens=set(tokens)

    #2. Crear la matriz de frecuencias de cada documento
    for i,libro in enumerate(books):

        tokens_libro = libro

        for token in tokens:
            if token not in frecuencia:
                frecuencia[token] = {textos[i]: 0}
            else:
                frecuencia[token][textos[i]] = 0

        for token_libro in tokens_libro:
            if token_libro in frecuencia:
                frecuencia[token_libro][textos[i]] += 1

    frecuencia= dict(sorted(frecuencia.items()))
    return frecuencia

def df(books) -> dict:
    pesos={}
    for i in books:
        lista=set(i)
        for j in lista:
            if j not in pesos:
                pesos[j]=1
            else:
                pesos[j]+=1

    pesos=dict(sorted(pesos.items()))
    return pesos

# La norma se saca a partir de los pesos tf-idf
def norma(tf,idf,collection_text) -> dict:
    length={}
    TF = np.array([[tf[token][collection_text[i]] for token in tf] for i,tokens in enumerate(collection_text)])
    IDF = np.array([idf[token] for token in idf])
    
    TF_IDF=TF*IDF

    for i,book in enumerate(collection_text):
        length[book]=np.linalg.norm(TF_IDF[i])

    return length