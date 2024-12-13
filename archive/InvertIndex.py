# import concurrent.futures # para procesamiento paralelo
# import os
# import json
# import math
# import numpy as np
# from ..utils.preprocesar import preprocesamiento
# from ..utils.tf_idf import tf_dic, idf_dic, tf, df, norma
# class InvertIndex:
#     def __init__(self, index_file) -> None:
#         self.index_file = os.path.join("data",index_file) #Para guardar el archivo en la carpeta data
#         self.index = {}
#         self.idf = {}
#         self.length = {}
#     def load_index(self, index_file) -> None:
#         try:
#             with open(index_file, 'r') as f:
#                 data = json.load(f)
#                 self.index = data['index']
#                 self.idf = data['idf']
#                 self.length = data['length']
#         except FileNotFoundError:
#             print("El archivo de índice no existe. Debe construirlo primero usando la función `building`.") 

#     def building(self, collection_text) -> None:
#         # Procesamiento en paralelo
#         def process_file(file_name):
#             with open( file_name, 'r') as file:
#                 texto = file.read().rstrip()
#                 return preprocesamiento(texto)

#         # Procesamiento paralelo para leer y preprocesar los documentos
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             textos_procesados = list(executor.map(process_file, collection_text))

#         # compute the tf
#         self.index=tf_dic(tf(textos_procesados,collection_text))

#         # compute the idf
#         self.idf=idf_dic(df(textos_procesados),len(textos_procesados))
    
#         # compute the length (norm)
#         self.length=norma(self.index,self.idf,collection_text)

#         # store in disk
#         data = {
#             'index': self.index,
#             'idf': self.idf,
#             'length': self.length
#         }
#         with open(self.index_file, 'w') as f:
#             json.dump(data, f)
    
#     def validate_query(self, query_term_unic) -> set:
#         aux = set()
#         for term in query_term_unic:
#         # Validamos si existe el término en nuestros diccionarios
#             if term in self.idf:
#                 aux.add(term)
#         return aux
    
#     def retrieval(self, query, k) -> list:
#         self.load_index(self.index_file)
#         # preprocesar la query: extraer los terminos unicos
#         queryPrep = preprocesamiento(query)
#         query_term_unic=set(queryPrep)

#         # diccionario para el score
#         score = {}
#         # aplicar similitud de coseno y guardarlo en el diccionario score
#         for key in self.length.keys():
#             score[key] = 0
#         #validamos si existe el termino en nuestros diccionarios
#         query_term_unic=self.validate_query(query_term_unic)
#         if(len(query_term_unic)==0):
#             return score

#         lenght_query=[]

#         for term in query_term_unic:
#             # calcular el tf-idf del query
#             term_tf = math.log10(1+queryPrep.count(term))
#             term_idf = self.idf[term]
#             term_doc = self.index[term]

#             lenght_query.append(term_tf*term_idf)

#             for doc in term_doc:
#                 w_td = self.index[term][doc]*term_idf
#                 w_tq = term_tf*term_idf
#                 score[doc] += w_td * w_tq

#         norma_query=np.linalg.norm(np.array(lenght_query))

#         for doc in score:
#             score[doc] /= (self.length[doc]*norma_query)
#             score[doc] = round(score[doc], 2)


#         # ordenar el score de forma descendente
#         result = sorted(score.items(), key= lambda tup: tup[1], reverse=True)
#         # retornamos los k documentos mas relevantes (de mayor similitud al query)
#         return result[:k] 