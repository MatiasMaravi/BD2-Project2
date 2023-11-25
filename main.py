from src.classes.SPIMI import BSBI
from src.utils.building import building, retrieval
import time
import sys

def crear_indice():
    tiempo_inicial = time.time()
    Indice = BSBI(size_block=40960,archivo="spotify_songs.csv",funcion_sizeof=sys.getsizeof)
    Indice.SPIMI()
    Indice.merge_index()
    building()
    tiempo_final = time.time()
    print("indice creado en: ",tiempo_final-tiempo_inicial," segundos")

<<<<<<< HEAD
def realizar_consulta():
    import os
    if not os.path.exists("blocks_index"):
        print("No existe el indice invertido, por favor cree el indice primero")
        return
    consulta = input("Ingrese la consulta: ")
    k = int(input("Ingrese el numero de resultados: "))
    resultado = retrieval(consulta,k)
    print(resultado)
=======
Indice=BSBI(size_block=40960,archivo="spotify_songs.csv",funcion_sizeof=sys.getsizeof)
Indice.SPIMI()

Indice.merge_index()
Indice.building()

tiempo_final = time.time()

tiempo_ejecucion = tiempo_final - tiempo_inicial

print('El tiempo de ejecucion fue:',tiempo_ejecucion,'segundos')

# Probamos el indice con una consulta

resultado=Indice.retrieval("", 10)
print(resultado)
>>>>>>> 69c83a0 ( Documentacion del indice invertido terminada)


def menu():
    print("1. Crear Indice Invertido")
    print("2. Realizar Consulta")
    print("3. Salir")
    opcion = int(input("Ingrese una opcion: "))
    if opcion == 1:
        crear_indice()
        input("Presione enter para continuar")
        menu()
    elif opcion == 2:
        realizar_consulta()
        input("Presione enter para continuar")
        menu()
    elif opcion == 3:
        print("Adios")
        
if __name__ == "__main__":
    menu()
