import nltk
from nltk.stem.snowball import SnowballStemmer
import sys
import json
import os
from collections import defaultdict
import pandas as pd


class BSBI:
    def __init__(self, size_block, archivo):
        self.size_block = size_block
        self.num_block = 0
        self.current_block = {}
        self.blocks = []
        self.archivo=archivo

    def SPIMI(self):
        # Cargamos la stoplist
        with open(os.path.join('Indice_invertido', 'stoplist.txt'), encoding='utf-8', ) as file:
                stoplist = [line.rstrip().lower() for line in file]
        stemmer = SnowballStemmer("english") # Verificar si las palabras estan en ingles


        with open(os.path.abspath(self.archivo)) as f:
            next(f)
            df = pd.read_csv(self.archivo)

            i=0

            for line in f:

                tokens = [stemmer.stem(word.lower()) for word in nltk.word_tokenize(line) if word.isalpha() and word.lower() not in stoplist]

                # Calculamos el tf, guardaremos solo este valor debido a que el df se calcula en la fase de merge, con todos los bloques

                tf = defaultdict(lambda: defaultdict(int))

                for token in tokens:
                    tf[token][df.loc[i,"track_id"]] += 1

                # Añadimos los tf al bloque actual
                for token in tf:
                    if token in self.current_block:
                        for doc in tf[token]:
                            self.current_block[token][doc] += tf[token][doc]
                    else:
                        self.current_block[token] = tf[token]


                self.current_block = dict(sorted(self.current_block.items()))
                i+=1        
                
                if(i==100):
                    break
                # Si el tamaño del bloque es igual al tamaño de bloque que se ha definido, se guarda el bloque en la lista de bloques
                if sys.getsizeof(self.current_block) >= self.size_block:
                    self.num_block += 1
                    self.save_block("blocks_index",self.num_block,self.current_block)
                    self.blocks.append('block' + str(self.num_block) + '.json')
                    self.current_block = {}

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

        
        potencia_2=1
        final=0

        while(potencia_2<=num_blocks_merge):
            potencia_2=potencia_2*2
            final+=1


       
        # Gestiona desde donde se empieza a recorrer los bloques de la derecha y de la izquierda
        # bloques_inicio: desde donde se empieza a recorrer los bloques de la izquierda
        # bloques_final: desde donde se empieza a recorrer los bloques de la derecha
        for p in range(0,final):
            b=2**p
            bloques_inicio=0
            bloques_final=b
            self.left_merged = {}
            self.right_merged = {}
            
            # Recorre los bloques de la derecha y de la izquierda, por todos los bloques
            while(bloques_inicio<potencia_2-b and bloques_final<potencia_2):
                self.i=bloques_inicio
                self.j=bloques_final
                print("bloques_inicio: ",bloques_inicio)
                print("bloques_final: ",bloques_final)

                # Crea un diccionario vacio para guardar el diccionario ordenado
                self.sorted_dict = {}

                # Recorre cada caso de bloque a la derecha y a la izquierda
                while(self.i<bloques_final and self.j<bloques_final+b):

                    # Verificamos que el archivo de los bloques exista
                    if(self.i<len(self.blocks) and (self.j<len(self.blocks))):
                        print("i: ",self.i,self.blocks[self.i])
                        print("j: ",self.j,self.blocks[self.j])
                        # Caso en el que los dos bloques se quedan vacios
                        if(len(self.left_merged)==0 and len(self.right_merged)==0):
                            with open("blocks_index/" + self.blocks[self.i], "rb") as f:
                                self.left_merged = json.load(f)

                            with open("blocks_index/" + self.blocks[self.j], "rb") as f:
                                self.right_merged = json.load(f)

                            self.merge_dicts()

                        # Caso en el que el bloque de la izquierda se queda vacio
                        elif(len(self.left_merged)==0):
                            with open("blocks_index/" + self.blocks[self.i], "rb") as f:
                                self.left_merged = json.load(f)

                            self.merge_dicts()

                        # Caso en el que el bloque de la derecha se queda vacio
                        elif(len(self.right_merged)==0):
                            with open("blocks_index/" + self.blocks[self.j], "rb") as f:
                                self.right_merged = json.load(f)

                            self.merge_dicts()

                    else:
                        if(self.i<bloques_final):
                            print("entro_sin_comparar_izquierda")
                            dict_= {**self.sorted_dict,**self.left_merged}
                            self.left_merged = {}
                            self.sorted_dict = {}
                            while(self.i<bloques_final and self.i<len(self.blocks)):
                                with open("blocks_index/" + self.blocks[self.i], "rb") as f:    
                                    bloque_izquierda_faltante = json.load(f)
                                    for key in bloque_izquierda_faltante:
                                        dict_[key]=bloque_izquierda_faltante[key]

                                        if sys.getsizeof(dict_) >= self.size_block:
                                            self.num_block += 1
                                            self.save_block("blocks_merge",self.num_block,dict_)
                                            dict_ = {}

                                self.i+=1            
                                        
                        elif(self.j<bloques_final+b):
                            print("entro_sin_comarar_derecha")
                            dict_= {**self.sorted_dict,**self.right_merged}
                            self.right_merged = {}
                            self.sorted_dict = {}
                            while(self.j<bloques_final+b and self.j<len(self.blocks)):
                                with open("blocks_index/" + self.blocks[self.j], "rb") as f:    
                                    bloque_derecha_faltante = json.load(f)
                                    for key in bloque_derecha_faltante:
                                        dict_[key]=bloque_derecha_faltante[key]

                                        if sys.getsizeof(dict_) >= self.size_block:
                                            self.num_block += 1
                                            self.save_block("blocks_merge",self.num_block,dict_)
                                            dict_ = {}

                                self.j+=1            
                        break  

                # Verificaciones luego de que se hayan recorrido los bloques    
                # Si un bloque que se cargo aun tiene elementos, se guarda en un nuevo bloque( Posible error al momento de ordenar)

                if(len(self.left_merged)!=0):
                    print("entro_left")
                    self.num_block += 1
                    guardar={**self.sorted_dict,**self.left_merged}
                    self.save_block("blocks_merge",self.num_block,guardar)
                    self.left_merged = {}

                elif(len(self.right_merged)!=0):
                    print("entro_right")
                    self.num_block += 1
                    guardar={**self.sorted_dict,**self.right_merged}
                    self.save_block("blocks_merge",self.num_block,guardar)
                    self.right_merged = {}
                

                """if(self.i==bloques_final):
                    print("i:", self.i)

                    while(self.j<bloques_final+b and self.j<len(self.blocks)):
                        print("entro_bloque_derecha")
                        with open("blocks_index/" + self.blocks[self.j], "rb") as f:
                            self.right_merged = json.load(f)
                            self.num_block += 1
                            self.save_block("blocks_merge",self.num_block,self.right_merged)
                            self.right_merged = {}

                        self.j+=1      

                elif(self.j==bloques_final+b):
                    print("j:", self.j)

                    while(self.i<bloques_final and self.i<len(self.blocks)):
                        print("entro_bloque_izquierda")
                        with open("blocks_index/" + self.blocks[self.i], "rb") as f:
                            self.left_merged = json.load(f)
                            self.num_block += 1
                            self.save_block("blocks_merge",self.num_block,self.left_merged)
                            self.left_merged = {}   
                        self.i+=1 """



                print()
                bloques_inicio=bloques_final+b
                bloques_final= bloques_inicio+b

            self.verificacion_archivos()
            self.actualizar_blocks()
            print(self.num_block)
            self.blocks=self.blocks[:self.num_block]
            print
            self.num_block=0
            print()
            
            if(p==3):
                break



    def merge_dicts(self):
        # Obtenemos las claves de ambos diccionarios
        keys1 = list(self.left_merged.keys())
        keys2 = list(self.right_merged.keys())

        # Aplicamos Merge Sort a las claves
        sorted_keys = self.merge(keys1, keys2)


        for key in sorted_keys:

            if (len(self.left_merged)!=0 and len(self.right_merged)!=0): # Verificamos si alguno de los dos diccionarios se quedo vacio, para agregar un diccionario del lado que quedo vacio
                
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

                if sys.getsizeof(self.sorted_dict) >= self.size_block:
                    print("entro_escribir")
                    self.num_block += 1
                    self.save_block("blocks_merge",self.num_block,self.sorted_dict)
                    self.sorted_dict = {}

            else:
                if(len(self.left_merged)==0):
                    print("entro_izquierda")
                    self.i+=1

                elif(len(self.right_merged)==0):
                    print("aumento_derecha")
                    self.j+=1

                break        

        
    
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

    def verificacion_archivos(self):
        directorio = "blocks_merge"
        archivos = os.listdir(directorio)

        for archivo in archivos:
            if archivo not in self.blocks:
                os.remove("blocks_merge/" + archivo)


        

# 0 1 , 0 2, 0 4

# molestart

            
    






""" def merge(self, dict1, dict2):
    # Función para fusionar dos diccionarios
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if key in merged_dict:
            if isinstance(value, dict) and isinstance(merged_dict[key], dict):
                merged_dict[key] = self.merge(merged_dict[key], value)
            elif isinstance(value, int) and isinstance(merged_dict[key], int):
                merged_dict[key] += value
        else:
            merged_dict[key] = value
    return dict(sorted(merged_dict.items()))

def merge_blocks(self,blocks):
    # Caso base: si solo hay un bloque, devolver el índice invertido de ese bloque
    if len(blocks) == 1:
        with open("blocks/" + blocks[0], "rb") as f:
            return json.load(f)
    
    # Divide los bloques en dos grupos aproximadamente iguales
    mid = len(blocks) // 2
    left_blocks = blocks[:mid]
    right_blocks = blocks[mid:]
    
    # Fusiona recursivamente los bloques en cada grupo
    left_merged = self.merge_blocks(left_blocks)
    right_merged = self.merge_blocks(right_blocks)
    
    # Fusiona los resultados de los grupos
    merged_index = self.merge(left_merged, right_merged)
    
    return merged_index

def init_merge(self):
    return self.merge_blocks(self.blocks)
def delete_blocks(self):
    # Elimina todos los bloques
    for block in self.blocks:
        os.remove("blocks/" + block)
    self.blocks = []
    self.block = 0
def equilibrar_blocks(self, index):
    with open(index, encoding='utf-8', ) as file:
        index = json.load(file)
        self.current_block = {}
        for i in index.keys():
            self.current_block[i] = index[i]
            if(sys.getsizeof(self.current_block) >= self.size_block):
                self.block += 1
                self.save_block()
                self.current_block = {}
        if self.current_block:
            self.block += 1
            self.save_block()
            self.current_block = {}"""