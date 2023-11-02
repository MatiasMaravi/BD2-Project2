import os
import json
from SPIMI import BSBI

# Construimos el indice

Indice=BSBI(size_block=20480,archivo="spotify_songs.csv")
Indice.SPIMI()
merged_index = Indice.init_merge()
Indice.delete_blocks()
# Guarda el índice invertido fusionado en un archivo JSON
with open("index.json", "w") as f:
    json.dump(merged_index, f, indent=4, ensure_ascii=False)

print("Índice invertido fusionado guardado en index.json")
Indice.equilibrar_blocks("index.json")