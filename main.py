import os
import json
from SPIMI import BSBI
import time
import sys
from pympler import asizeof
# Construimos el indice

tiempo_inicial = time.time()

Indice=BSBI(size_block=40960,archivo="spotify_songs.csv",funcion_sizeof=sys.getsizeof)
Indice.SPIMI()

Indice.merge_index()
Indice.building()

tiempo_final = time.time()

tiempo_ejecucion = tiempo_final - tiempo_inicial

print('El tiempo de ejecucion fue:',tiempo_ejecucion,'segundos')


