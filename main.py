import os
from SPIMI import BSBI

# Construimos el indice

Indice=BSBI(size_block=20480,archivo="spotify_songs.csv")
Indice.SPIMI()
