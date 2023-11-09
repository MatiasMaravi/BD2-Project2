import nltk
from nltk.stem.snowball import SnowballStemmer
import sys
import json
import os
from pympler  import asizeof
from collections import defaultdict
import pandas as pd
import numpy as np
import math


class BSBI:
    def __init__(self, size_block, archivo,funcion_sizeof):
        self.size_block = size_block
        self.num_block = 0
        self.current_block = {}
        self.blocks = []
        self.archivo=archivo
        self.funcion_sizeof=funcion_sizeof
        self.num_books=0
        self.books=[]

    def SPIMI(self):
        # Cargamos la stoplist
        with open(os.path.join('Indice_invertido', 'stoplist.txt'), encoding='utf-8', ) as file:
                stoplist = [line.rstrip().lower() for line in file]
        stemmer = SnowballStemmer("english") # Verificar si las palabras estan en ingles


        with open(os.path.abspath(self.archivo)) as f:
            next(f)
            df = pd.read_csv(self.archivo)

            for line in f:

                tokens = [stemmer.stem(word.lower()) for word in nltk.word_tokenize(line) if word.isalpha() and word.lower() not in stoplist]

                # Calculamos el tf, guardaremos solo este valor debido a que el df se calcula en la fase de merge, con todos los bloques

                tf = defaultdict(lambda: defaultdict(int))

                self.books.append(df.loc[self.num_books,"track_id"])
                for token in tokens:
                    tf[token][df.loc[self.num_books,"track_id"]] += 1

                # Añadimos los tf al bloque actual
                for token in tf:
                    if token in self.current_block:
                        for doc in tf[token]:
                            self.current_block[token][doc] += tf[token][doc]
                    else:
                        self.current_block[token] = tf[token]


                self.current_block = dict(sorted(self.current_block.items()))

                # Si el tamaño del bloque es igual al tamaño de bloque que se ha definido, se guarda el bloque en la lista de bloques
                if self.funcion_sizeof(self.current_block) >= self.size_block:
                    self.num_block += 1
                    self.save_block("blocks_index",self.num_block,self.current_block)
                    self.blocks.append('block' + str(self.num_block) + '.json')
                    self.current_block = {}

                self.num_books += 1

        if self.current_block:
            self.num_block += 1
            self.save_block("blocks_index",self.num_block,self.current_block)
            self.blocks.append('block' + str(self.num_block) + '.json')
            self.current_block = {}

        print(self.blocks)                


    def save_block(self,nombre_carpeta,num_block,bloque):
            # Nombre del archivo dentro de la carpeta
            nombre_archivo = 'block' + str(num_block) + '.json'
            
            # Combinar la carpeta y el nombre de archivo para obtener la ruta completa
            ruta_completa = os.path.join(nombre_carpeta, nombre_archivo)

            # Asegúrate de que la carpeta exista antes de guardar el archivo
            if not os.path.exists(nombre_carpeta):
                os.makedirs(nombre_carpeta)

            with open(ruta_completa, 'w',encoding="utf-8") as f:
                json.dump(bloque, f,ensure_ascii=False, indent=4)            




    # Ordena los bloques y los fusiona en un solo índice invertido global que sigue dividido en bloques

    def merge_index(self):

        num_blocks_merge= self.num_block

        self.num_block = 0

        # Si solo hay un bloque, devolver el índice invertido de ese bloque

        if num_blocks_merge == 1:
            with open("blocks_index/" + self.blocks[0], "rb") as f:
                diccionario= json.load(f)

            self.num_block += 1
            self.save_block("blocks_merge",self.num_block,diccionario)
            return  

        # Divide en dos grupos iguales
        
        final=self.calcular_cuadrado(num_blocks_merge)
        print(final)
        potencia_2=2**final
        print(potencia_2)
       
        # Gestiona desde donde se empieza a recorrer los bloques de la derecha y de la izquierda
        # bloques_inicio: desde donde se empieza a recorrer los bloques de la izquierda
        # bloques_final: desde donde se empieza a recorrer los bloques de la derecha

        for p in range(0,final):
            b=2**p
            bloques_inicio_izquierda=0
            bloques_inicio_derecha=b
            self.left_merged = {}
            self.right_merged = {}

            print("nivel",p)
            
            # Recorre los bloques de la derecha y de la izquierda, por todos los bloques
            while(bloques_inicio_izquierda<potencia_2-b and bloques_inicio_derecha<potencia_2):
                self.i=bloques_inicio_izquierda
                self.j=bloques_inicio_derecha

                print("bloques_inicio_izquierda",bloques_inicio_izquierda)
                print("bloques_inicio_derecha",bloques_inicio_derecha)
                print()

                # Crea un diccionario vacio para guardar el diccionario ordenado
                self.sorted_dict = {}
                self.left_merged = {}
                self.right_merged = {}
                self.guardar = {}
                self.contador_block=0
                # Recorre cada caso de bloque a la derecha y a la izquierda
                while(self.i<bloques_inicio_derecha and self.j<bloques_inicio_derecha+b):
                    # Verificamos que el archivo de los bloques exista
                    if(self.i<len(self.blocks) and (self.j<len(self.blocks))):
                        print("i",self.i," ", self.blocks[self.i])
                        print("j",self.j," ", self.blocks[self.j])

                        # Caso en el que los dos bloques se quedan vacios
                        if(len(self.left_merged)==0 and len(self.right_merged)==0):
                            print("entro")
                            file_path = os.path.join("blocks_index", self.blocks[self.i])
                            with open(file_path, "rb") as f:
                                self.left_merged = json.load(f)


                            file_path = os.path.join("blocks_index", self.blocks[self.j])
                            with open(file_path, "rb") as f:
                                self.right_merged = json.load(f)

                                self.merge_dicts()

                        # Caso en el que el bloque de la izquierda se queda vacio
                        elif(len(self.left_merged)==0):
                            print("entrar_izquierda")
                            with open("blocks_index/" + self.blocks[self.i], "rb") as f:
                                self.left_merged = json.load(f)

                            self.merge_dicts()

                        # Caso en el que el bloque de la derecha se queda vacio
                        elif(len(self.right_merged)==0):
                            with open("blocks_index/" + self.blocks[self.j], "rb") as f:
                                self.right_merged = json.load(f)

                            self.merge_dicts()

                    # Bien hasta aqui, dinamismo al comparar entre bloques    
                    else:
                        break

                # Verificaciones luego de salida del while, para ver si quedaron bloques sin comparar

                # Rellenamos los datos que quedan en el diccionario ordenado y lo que se cargo en alguno de los dos diccionarios
                if(len(self.left_merged)!=0):
                    self.guardar={**self.sorted_dict,**self.left_merged}
                    self.contador_block+=1
                    self.num_block += 1
                    self.save_block("blocks_merge",self.num_block,self.guardar)
                    self.guardar = {}
                    self.left_merged = {}
                    self.sorted_dict = {}
                    self.i+=1                

                elif(len(self.right_merged)!=0):
                    self.guardar={**self.sorted_dict,**self.right_merged}
                    self.contador_block+=1
                    self.num_block += 1
                    self.save_block("blocks_merge",self.num_block,self.guardar)
                    self.guardar = {}
                    self.right_merged = {}
                    self.sorted_dict = {}
                    self.j+=1

                # Rellenamos la data de los bloques que no se compararon

             
                if(self.i<bloques_inicio_derecha and self.i<len(self.blocks)):
                    while(self.i<bloques_inicio_derecha and self.i<len(self.blocks)):
                        with open("blocks_index/" + self.blocks[self.i], "rb") as f:    
                            bloque_izquierda_faltante = json.load(f)
                            self.guardar={**self.guardar,**bloque_izquierda_faltante}
                            self.contador_block+=1
                            self.num_block += 1
                            self.save_block("blocks_merge",self.num_block,self.guardar)
                            self.guardar = {}   

                        self.i+=1


                elif(self.j<bloques_inicio_derecha+b and self.j<len(self.blocks)):
                    while(self.j<bloques_inicio_derecha+b and self.j<len(self.blocks)):
                        with open("blocks_index/" + self.blocks[self.j], "rb") as f:    
                            bloque_derecha_faltante = json.load(f)
                            self.guardar={**self.guardar,**bloque_derecha_faltante}
                            self.contador_block+=1
                            self.num_block += 1
                            self.save_block("blocks_merge",self.num_block,self.guardar)
                            self.guardar = {}

                        self.j+=1

                if self.guardar:
                    self.contador_block+=1
                    self.num_block += 1
                    self.save_block("blocks_merge",self.num_block,self.guardar)
                    self.guardar = {}

                if self.contador_block<2*b:
                    while self.contador_block<2*b:
                        self.num_block += 1
                        self.save_block("blocks_merge",self.num_block,self.guardar)
                        self.guardar = {}
                        self.contador_block+=1                        
    
                bloques_inicio_izquierda=bloques_inicio_derecha+b
                bloques_inicio_derecha= bloques_inicio_izquierda+b

            self.actualizar_blocks()
            self.blocks=self.blocks[:self.num_block]
            self.num_block=0

        self.eliminar_archivos_vacios("blocks_index")    
  

    def calcular_cuadrado(self, num_blocks_merge):
        final=0

        while(2**final<num_blocks_merge):
            final+=1

        return final            



    def merge_dicts(self):
        # Obtenemos las claves de ambos diccionarios
        keys1 = list(self.left_merged.keys())
        keys2 = list(self.right_merged.keys())

        # Aplicamos Merge Sort a las claves
        sorted_keys = self.merge(keys1, keys2)

        print("tamaño_left: ", len(self.left_merged))
        print("tamaño_rigth: ", len(self.right_merged))
        for key in sorted_keys:
            if (len(self.left_merged)!=0 and len(self.right_merged)!=0): # Verificamos si alguno de los dos diccionarios se quedo vacio, para agregar un diccionario del lado que quedo

                if key in self.left_merged and key in self.right_merged:
                    self.sorted_dict[key] = {**self.left_merged[key], **self.right_merged[key]}
                    del self.left_merged[key]
                    del self.right_merged[key]

                elif key in self.left_merged:
                    self.sorted_dict[key] = self.left_merged[key]
                    del self.left_merged[key]
                else:
                    self.sorted_dict[key] = self.right_merged[key]
                    del self.right_merged[key]

                if self.funcion_sizeof(self.sorted_dict) >= self.size_block:
                    self.contador_block+=1
                    self.num_block += 1
                    self.save_block("blocks_merge",self.num_block,self.sorted_dict)
                    self.sorted_dict = {}
                  
            else:
                print("entro_else")
                if(len(self.left_merged)==0 and len(self.right_merged)==0):
                    print("aumento i y j")
                    print()
                    self.i+=1
                    self.j+=1
                    break

                elif(len(self.left_merged)==0):
                    print("aumento i")
                    print()
                    self.i+=1
                    break

                elif(len(self.right_merged)==0):
                    print("aumento j")
                    print()
                    self.j+=1
                    break

                break        
    
        if(len(self.left_merged)==0 and len(self.right_merged)==0):
            print("SE ACABO LA DATA")
            self.i+=1
            self.j+=1

            self.contador_block+=1
            self.num_block += 1
            self.save_block("blocks_merge",self.num_block,self.sorted_dict)
            self.sorted_dict = {}


    
    def merge(self,arr1, arr2):
        merged = []
        i, j = 0, 0

        while i < len(arr1) and j < len(arr2):
            if arr1[i] < arr2[j]:
                merged.append(arr1[i])
                i += 1
            elif arr1[i] > arr2[j]:
                merged.append(arr2[j])
                j += 1
            else:
                # Si los elementos son iguales, agregar uno de ellos a merged
                merged.append(arr1[i])
                i += 1
                j += 1

        # Agregar cualquier elemento restante de arr1 y arr2
        merged.extend(arr1[i:])
        merged.extend(arr2[j:])

        return merged
        

    def actualizar_blocks(self):

        import shutil
        import os
        carpeta_origen = "blocks_merge"
        carpeta_destino = "blocks_index"

        shutil.rmtree(carpeta_destino)

        os.rename(carpeta_origen, carpeta_destino)

        print("Archivos actualizados")

    def eliminar_archivos_vacios(self,ruta_carpeta):
        for nombre_archivo in os.listdir(ruta_carpeta):
            ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
            if os.path.isfile(ruta_archivo):
                with open(ruta_archivo, 'r') as archivo:
                    contenido = archivo.read()
                    try:
                        datos = json.loads(contenido)
                        if isinstance(datos, dict) and not datos:
                            # Si el archivo contiene un diccionario vacío, eliminarlo
                            os.remove(ruta_archivo)
                            print(f"Se eliminó el archivo: {nombre_archivo}")
                    except json.JSONDecodeError:
                        pass


    def building(self):
        #Construimos el resto del indice invertido
        

        # TF

        #Actualizamos todos los valores de los tfs en el indice invertido global

        # Cargamos el indice invertido global por bloques

        carpeta = "blocks_index"

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

        div = math.log10(self.num_books)

        for token in df:
            df[token] = div - math.log10(df[token])

        # Guardamos el idf en un archivo
        with open("idf.json", "w") as f:
            json.dump(df, f,ensure_ascii=False, indent=4)

        print("IDF calculado")    

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
            if len(norma[key])<len(self.books):
                norma[key].extend([0]*(len(self.books)-len(norma[key])))

        for key in norma:
            norma[key] = np.linalg.norm(np.array(norma[key]))        

        """for book in self.books:
            TF_IDF = []
            for nombre_archivo in os.listdir(carpeta):
                ruta_archivo = os.path.join(carpeta, nombre_archivo)
                if os.path.isfile(ruta_archivo):
                    with open(ruta_archivo, "r") as f:
                        index_temp = json.load(f)
                        TF_IDF.extend([index_temp[token][book] * df[token] if book in index_temp[token] else 0 for token in index_temp])
            TF_IDF = np.array(TF_IDF)
            norma[book] = np.linalg.norm(TF_IDF)"""

        # Guardamos la norma en un archivo

        with open("norma.json", "w") as f:
            json.dump(norma, f,ensure_ascii=False, indent=4)

        print("Norma calculada")        

    def validate_query(self, query_term_unic,idf) -> set:
        aux = set()
        for term in query_term_unic:
        # Validamos si existe el término en nuestros diccionarios
            if term in idf:
                aux.add(term)
        return aux        


    def retrieval(self, query, k) -> list:

        stemmer = SnowballStemmer("english") # Verificar si las palabras estan en ingles

        with open(os.path.join('Indice_invertido', 'stoplist.txt'), encoding='utf-8', ) as file:
                stoplist = [line.rstrip().lower() for line in file]

        queryPrep = [stemmer.stem(word.lower()) for word in nltk.word_tokenize(query) if word.isalpha() and word.lower() not in stoplist]

        query_term_unic=set(queryPrep)

        # Cargamos el idf y la norma

        with open("idf.json", "r") as f:
            idf = json.load(f)

        with open("norma.json", "r") as f:
            norma = json.load(f)     

        score = {}

        for key in norma.keys():
            score[key] = 0

        # Validamos si existe el termino en nuestros diccionarios
        query_term_unic=self.validate_query(query_term_unic,idf)

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

