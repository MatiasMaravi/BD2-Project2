import json
import os
from collections import defaultdict
import pandas as pd
from ..utils.preprocesamiento import preprocesamiento
from ..utils.aux import save_block, calcular_cuadrado, merge, actualizar_blocks, eliminar_archivos_vacios


class BSBI:
    def __init__(self, size_block, archivo, funcion_sizeof, carpeta):
        self.size_block = size_block
        self.num_block = 0
        self.current_block = {}
        self.blocks = []
        self.archivo = archivo
        self.funcion_sizeof = funcion_sizeof
        self.num_books = 0
        self.books = []
        self.carpeta = carpeta

    def SPIMI(self, idioma):
        # Cargamos la stoplist
        with open(os.path.abspath(self.archivo)) as f:
            next(f)
            df = pd.read_csv(self.archivo)

            for line in f:

                tokens = preprocesamiento(line, idioma)

                # Calculamos el tf, guardaremos solo este valor debido a que el df se calcula en la fase de merge, con todos los bloques

                tf = defaultdict(lambda: defaultdict(int))

                self.books.append(df.loc[self.num_books, "track_id"])
                for token in tokens:
                    tf[token][df.loc[self.num_books, "track_id"]] += 1

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
                    save_block(self.carpeta, self.num_block, self.current_block)
                    self.blocks.append('block' + str(self.num_block) + '.json')
                    self.current_block = {}

                self.num_books += 1

        if self.current_block:
            self.num_block += 1
            save_block(self.carpeta, self.num_block, self.current_block)
            self.blocks.append('block' + str(self.num_block) + '.json')
            self.current_block = {}

    # Ordena los bloques y los fusiona en un solo índice invertido global que sigue dividido en bloques

    def merge_index(self):

        num_blocks_merge = self.num_block

        self.num_block = 0

        # Si solo hay un bloque, devolver el índice invertido de ese bloque

        if num_blocks_merge == 1:
            with open(self.carpeta + '/' + self.blocks[0], "rb") as f:
                diccionario = json.load(f)

            self.num_block += 1
            save_block("blocks_merge", self.num_block, diccionario)
            return

            # Divide en dos grupos iguales
        final = calcular_cuadrado(num_blocks_merge)
        potencia_2 = 2 ** final
        # Gestiona desde donde se empieza a recorrer los bloques de la derecha y de la izquierda
        # bloques_inicio: desde donde se empieza a recorrer los bloques de la izquierda
        # bloques_final: desde donde se empieza a recorrer los bloques de la derecha

        for p in range(0, final):
            b = 2 ** p
            bloques_inicio_izquierda = 0
            bloques_inicio_derecha = b
            self.left_merged = {}
            self.right_merged = {}

            # Recorre los bloques de la derecha y de la izquierda, por todos los bloques
            while (bloques_inicio_izquierda < potencia_2 - b and bloques_inicio_derecha < potencia_2):
                self.i = bloques_inicio_izquierda
                self.j = bloques_inicio_derecha

                # Crea un diccionario vacio para guardar el diccionario ordenado
                self.sorted_dict = {}
                self.left_merged = {}
                self.right_merged = {}
                self.guardar = {}
                self.contador_block = 0
                # Recorre cada caso de bloque a la derecha y a la izquierda
                while (self.i < bloques_inicio_derecha and self.j < bloques_inicio_derecha + b):
                    # Verificamos que el archivo de los bloques exista
                    if (self.i < len(self.blocks) and (self.j < len(self.blocks))):
                        # Caso en el que los dos bloques se quedan vacios
                        if (len(self.left_merged) == 0 and len(self.right_merged) == 0):
                            file_path = os.path.join(self.carpeta, self.blocks[self.i])
                            with open(file_path, "rb") as f:
                                self.left_merged = json.load(f)

                            file_path = os.path.join(self.carpeta, self.blocks[self.j])
                            with open(file_path, "rb") as f:
                                self.right_merged = json.load(f)

                                self.merge_dicts()

                        # Caso en el que el bloque de la izquierda se queda vacio
                        elif (len(self.left_merged) == 0):

                            with open(self.carpeta + '/' + self.blocks[self.i], "rb") as f:
                                self.left_merged = json.load(f)

                            self.merge_dicts()

                        # Caso en el que el bloque de la derecha se queda vacio
                        elif (len(self.right_merged) == 0):
                            with open(self.carpeta + '/' + self.blocks[self.j], "rb") as f:
                                self.right_merged = json.load(f)

                            self.merge_dicts()

                    # Bien hasta aqui, dinamismo al comparar entre bloques
                    else:
                        break

                # Verificaciones luego de salida del while, para ver si quedaron bloques sin comparar

                # Rellenamos los datos que quedan en el diccionario ordenado y lo que se cargo en alguno de los dos diccionarios
                if (len(self.left_merged) != 0):
                    self.guardar = {**self.sorted_dict, **self.left_merged}
                    self.contador_block += 1
                    self.num_block += 1
                    save_block("blocks_merge", self.num_block, self.guardar)
                    self.guardar = {}
                    self.left_merged = {}
                    self.sorted_dict = {}
                    self.i += 1

                elif (len(self.right_merged) != 0):
                    self.guardar = {**self.sorted_dict, **self.right_merged}
                    self.contador_block += 1
                    self.num_block += 1
                    save_block("blocks_merge", self.num_block, self.guardar)
                    self.guardar = {}
                    self.right_merged = {}
                    self.sorted_dict = {}
                    self.j += 1

                # Rellenamos la data de los bloques que no se compararon

                if (self.i < bloques_inicio_derecha and self.i < len(self.blocks)):
                    while (self.i < bloques_inicio_derecha and self.i < len(self.blocks)):
                        with open(self.carpeta + '/' + self.blocks[self.i], "rb") as f:
                            bloque_izquierda_faltante = json.load(f)
                            self.guardar = {**self.guardar, **bloque_izquierda_faltante}
                            self.contador_block += 1
                            self.num_block += 1
                            save_block("blocks_merge", self.num_block, self.guardar)
                            self.guardar = {}

                        self.i += 1


                elif (self.j < bloques_inicio_derecha + b and self.j < len(self.blocks)):
                    while (self.j < bloques_inicio_derecha + b and self.j < len(self.blocks)):
                        with open(self.carpeta + '/' + self.blocks[self.j], "rb") as f:
                            bloque_derecha_faltante = json.load(f)
                            self.guardar = {**self.guardar, **bloque_derecha_faltante}
                            self.contador_block += 1
                            self.num_block += 1
                            save_block("blocks_merge", self.num_block, self.guardar)
                            self.guardar = {}

                        self.j += 1

                if self.guardar:
                    self.contador_block += 1
                    self.num_block += 1
                    save_block("blocks_merge", self.num_block, self.guardar)
                    self.guardar = {}

                if self.contador_block < 2 * b:
                    while self.contador_block < 2 * b:
                        self.num_block += 1
                        save_block("blocks_merge", self.num_block, self.guardar)
                        self.guardar = {}
                        self.contador_block += 1

                bloques_inicio_izquierda = bloques_inicio_derecha + b
                bloques_inicio_derecha = bloques_inicio_izquierda + b

            actualizar_blocks(self.carpeta)
            self.blocks = self.blocks[:self.num_block]
            self.num_block = 0

        eliminar_archivos_vacios(self.carpeta)

    def merge_dicts(self):
        # Obtenemos las claves de ambos diccionarios
        keys1 = list(self.left_merged.keys())
        keys2 = list(self.right_merged.keys())

        # Aplicamos Merge Sort a las claves
        sorted_keys = merge(keys1, keys2)

        for key in sorted_keys:
            if (len(self.left_merged) != 0 and len(
                    self.right_merged) != 0):  # Verificamos si alguno de los dos diccionarios se quedo vacio, para agregar un diccionario del lado que quedo

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
                    self.contador_block += 1
                    self.num_block += 1
                    save_block("blocks_merge", self.num_block, self.sorted_dict)
                    self.sorted_dict = {}
            else:
                if (len(self.left_merged) == 0 and len(self.right_merged) == 0):
                    self.i += 1
                    self.j += 1
                    break

                elif (len(self.left_merged) == 0):
                    self.i += 1
                    break

                elif (len(self.right_merged) == 0):
                    self.j += 1
                    break

                break

        if (len(self.left_merged) == 0 and len(self.right_merged) == 0):
            self.i += 1
            self.j += 1

            self.contador_block += 1
            self.num_block += 1
            save_block("blocks_merge", self.num_block, self.sorted_dict)
            self.sorted_dict = {}