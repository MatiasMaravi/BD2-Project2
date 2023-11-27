from src.classes.SPIMI import BSBI
from src.utils.building import building, retrieval
import time
import sys


def crear_indice(idioma):
    tiempo_inicial = time.time()
    Indice = BSBI(size_block=40960, archivo="new_spotify_songs_" + idioma + ".csv", funcion_sizeof=sys.getsizeof,
                  carpeta="blocks_" + idioma)
    Indice.SPIMI(idioma=idioma)
    Indice.merge_index()
    building(archivo="new_spotify_songs_" + idioma + ".csv", carpeta="blocks_" + idioma, idfname="idf_" + idioma,
             normaname="norma_" + idioma)
    tiempo_final = time.time()
    print("indice creado en: ", tiempo_final - tiempo_inicial, " segundos")


def realizar_consulta(idioma,consulta,topk):
    import os
    if not os.path.exists("blocks_" + idioma):
        print("No existe el indice invertido, por favor cree el indice primero")
        return

    resultado = retrieval(consulta, topk, "blocks_" + idioma, "idf_" + idioma, "norma_" + idioma, idioma)
    print(resultado)


def seleccionar_idioma():
    print("1. Español")
    print("2. Ingles")
    idioma = input("Ingrese el idioma: ")
    if idioma == "1":
        return "es"
    elif idioma == "2":
        return "en"
    else:
        print("Idioma no soportado")
        return seleccionar_idioma()


def menu():
    idioma = seleccionar_idioma()
    print("1. Crear Indice Invertido")
    print("2. Realizar Consulta")
    print("3. Salir")
    opcion = int(input("Ingrese una opcion: "))
    if opcion == 1:
        crear_indice(idioma)
        input("Presione enter para continuar")
        menu()
    elif opcion == 2:
        realizar_consulta(idioma)
        input("Presione enter para continuar")
        menu()
    elif opcion == 3:
        print("Adios")


if __name__ == "__main__":
    menu()