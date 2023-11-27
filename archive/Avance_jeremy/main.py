import random
import nltk
from nltk.corpus import words

nltk.download('words')
palabras_ingles = words.words()

"""Funcion de ordenar los terminos en orden"""

def orderbyAsc(collection):

    return sorted(collection)

def indice_invertido_escalable():
    nombre = random.choice(palabras_ingles)
    documento = random.randint(1, 100)
    tupla = (nombre, documento)
    return tupla

collect = [("Juan",5),("Maria",1),("Juan",2),("Pedro",3),("Luis",4),("Ana",5),("Jose",6)]
collect = [indice_invertido_escalable() for _ in range(100)]
print(orderbyAsc(collect))
