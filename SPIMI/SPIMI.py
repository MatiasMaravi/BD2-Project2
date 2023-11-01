import nltk
from nltk.stem.snowball import SnowballStemmer
import sys
import json
import os
from collections import defaultdict
import pandas as pd


class BSBI:

    def __init__(self, size_block,archivo):
        self.size_block = size_block
        self.block = 0
        self.current_block = {}
        self.blocks = []
        self.archivo=archivo

    def SPIMI(self):
        # Cargamos la stoplist
        with open(os.path.join('Indice_invertido', 'stoplist.txt'), encoding='latin1', ) as file:
                stoplist = [line.rstrip().lower() for line in file]
        stemmer = SnowballStemmer("spanish")


        with open(os.path.abspath(self.archivo)) as f:
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
                    self.block += 1
                    self.save_block()
                    self.current_block = {}

        # Guardamos el ultimo bloque
        if self.current_block:
            self.block += 1
            self.save_block()
            self.current_block = {}            

    def save_block(self):

            nombre_carpeta = "blocks"
            # Nombre del archivo dentro de la carpeta
            nombre_archivo = 'block' + str(self.block) + '.json'

            # Combinar la carpeta y el nombre de archivo para obtener la ruta completa
            ruta_completa = os.path.join(nombre_carpeta, nombre_archivo)

            # Asegúrate de que la carpeta exista antes de guardar el archivo
            if not os.path.exists(nombre_carpeta):
                os.makedirs(nombre_carpeta)

            with open(ruta_completa, 'w') as f:
                json.dump(self.current_block, f)          





                    





        