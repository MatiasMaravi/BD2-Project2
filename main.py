
import os
import json
from SPIMI import BSBI
import time
import sys
from pympler import asizeof
# Construimos el indice

tiempo_inicial = time.time()

Indice=BSBI(size_block=40960,archivo="spotify_songs.csv",funcion_sizeof=sys.getsizeof)
