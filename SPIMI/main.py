import os
from SPIMI import BSBI

# Construimos el indice

docs = os.listdir("doc")
Indice=BSBI(size_block=2048,files=docs)
Indice.SPIMI()
