    
import json
import os
import sys

def merge(self, dict1, dict2):
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

def merge_blocks(self, blocks):
    if os.path.exists(self.output_index_file):
        with open(self.output_index_file, "rb") as f:
            self.merged_index = json.load(f)
    else:
        self.merged_index = None

    # Caso base: si solo hay un bloque, devolver el índice invertido de ese bloque
    if len(blocks) == 1:
        with open("blocks_index/" + blocks[0], "rb") as f:
            self.merged_index = json.load(f)
    else:
        # Divide los bloques en dos grupos aproximadamente iguales
        mid = len(blocks) // 2
        left_blocks = blocks[:mid]
        right_blocks = blocks[mid:]

        # Fusiona recursivamente los bloques en cada grupo
        self.merge_blocks(left_blocks)
        left_merged = self.merged_index
        self.merge_blocks(right_blocks)
        right_merged = self.merged_index

        # Fusiona los resultados de los grupos
        self.merged_index = self.merge(left_merged, right_merged)

    if self.merged_index is not None:
        with open(self.output_index_file, "w") as f:
            json.dump(self.merged_index, f, indent=4, ensure_ascii=False)

def init_merge(self):
    self.merge_blocks(self.blocks)

def delete_blocks(self):
    # Elimina todos los bloques
    for block in self.blocks:
        os.remove("blocks_index/" + block)
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
            self.current_block = {}