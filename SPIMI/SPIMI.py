import nltk
from nltk.stem.snowball import SnowballStemmer
import sys
import json
import os
from collections import defaultdict


class BSBI:

    def __init__(self, size_block, files):
        self.size_block = size_block
        self.block = 0
        self.current_block = {}
        self.blocks = []
        self.files = files

    def SPIMI(self):
        # Cargamos la stoplist
        with open(os.path.join('Indice_invertido', 'stoplist.txt'), encoding='latin1', ) as file:
                stoplist = [line.rstrip().lower() for line in file]
        stemmer = SnowballStemmer("spanish")

        for file in self.files:
            with open(os.path.join('doc', file)) as f:
                tf = {}
                for line in f:
                    tokens = [stemmer.stem(word.lower()) for word in nltk.word_tokenize(line) if word.isalpha() and word.lower() not in stoplist]

                    # Calculamos el tf, guardaremos solo este valor debido a que el df se calcula en la fase de merge, con todos los bloques

                    tf = defaultdict(lambda: defaultdict(int))

                    for token in tokens:
                        tf[token][file] += 1

                    self.current_block.update(tf)
                    self.current_block = dict(sorted(self.current_block.items()))        
                    
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
            nombre_archivo = 'block' + str(self.block)

            # Combinar la carpeta y el nombre de archivo para obtener la ruta completa
            ruta_completa = os.path.join(nombre_carpeta, nombre_archivo)

            # Asegúrate de que la carpeta exista antes de guardar el archivo
            if not os.path.exists(nombre_carpeta):
                os.makedirs(nombre_carpeta)

            with open(ruta_completa, 'w') as f:
                json.dump(self.current_block, f)          





                    





        