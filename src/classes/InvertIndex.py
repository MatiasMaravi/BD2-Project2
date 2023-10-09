import concurrent.futures # para procesamiento paralelo
import os
import json
import math
import numpy as np
from ..utils.preprocesar import preprocesamiento
from ..utils.tf_idf import tf_dic, idf_dic, tf, df, norma
class InvertIndex:
    def __init__(self, index_file) -> None:
        self.index_file = index_file
        self.index = {}
        self.idf = {}
        self.length = {}
    def load_index(self, index_file):
        try:
            with open(index_file, 'r') as f:
                data = json.load(f)
                self.index = data['index']
                self.idf = data['idf']
                self.length = data['length']
        except FileNotFoundError:
            print("El archivo de índice no existe. Debe construirlo primero usando la función `building`.") 
    def building(self, collection_text):
        # Procesamiento en paralelo
        def process_file(file_name):
            with open(os.path.join("docs", file_name), 'r') as file:
                texto = file.read().rstrip()
                return preprocesamiento(texto)

        # Procesamiento paralelo para leer y preprocesar los documentos
        with concurrent.futures.ThreadPoolExecutor() as executor:
            textos_procesados = list(executor.map(process_file, collection_text))

        # compute the tf
        self.index=tf_dic(tf(textos_procesados,collection_text))

        # compute the idf
        self.idf=idf_dic(df(textos_procesados),len(textos_procesados))
    
        # compute the length (norm)
        self.length=norma(self.index,self.idf,collection_text)

        # store in disk
        data = {
            'index': self.index,
            'idf': self.idf,
            'length': self.length
        }
        with open(self.index_file, 'w') as f:
            json.dump(data, f)
            
    def retrieval(self, query, k):
        self.load_index(self.index_file)
        # diccionario para el score
        score = {}
        # preprocesar la query: extraer los terminos unicos
        queryPrep = preprocesamiento(query)
        # aplicar similitud de coseno y guardarlo en el diccionario score
        for key in self.length.keys():
            score[key] = 0

        query_term_unic=set(queryPrep)

        lenght_query=[]

        for term in query_term_unic:
            # Validamos si existe el término en nuestros diccionarios
            if term not in self.idf and term not in self.index:
                continue

            # calcular el tf-idf del query
            term_tf = math.log10(1+queryPrep.count(term))

            term_idf = self.idf[term]
            term_doc = self.index[term]

            lenght_query.append(term_tf*term_idf)

            for doc in term_doc:
                score[doc] += self.index[term][doc]*term_idf*term_tf*term_idf

        norma_query=np.linalg.norm(np.array(lenght_query))

        for doc in score:
            score[doc] /= (self.length[doc]*norma_query)
            score[doc] = round(score[doc], 2)


        # ordenar el score de forma descendente
        result = sorted(score.items(), key= lambda tup: tup[1], reverse=True)
        # retornamos los k documentos mas relevantes (de mayor similitud al query)
        return result[:k] 