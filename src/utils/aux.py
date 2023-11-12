import os
import json
def merge(arr1, arr2):
    merged = []
    i, j = 0, 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged.append(arr1[i])
            i += 1
        elif arr1[i] > arr2[j]:
            merged.append(arr2[j])
            j += 1
        else:
            # Si los elementos son iguales, agregar uno de ellos a merged
            merged.append(arr1[i])
            i += 1
            j += 1

    # Agregar cualquier elemento restante de arr1 y arr2
    merged.extend(arr1[i:])
    merged.extend(arr2[j:])

    return merged


def actualizar_blocks():

    import shutil
    import os
    carpeta_origen = "blocks_merge"
    carpeta_destino = "blocks_index"

    shutil.rmtree(carpeta_destino)

    os.rename(carpeta_origen, carpeta_destino)

    print("Archivos actualizados")

def eliminar_archivos_vacios(ruta_carpeta):
    for nombre_archivo in os.listdir(ruta_carpeta):
        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, 'r') as archivo:
                contenido = archivo.read()
                try:
                    datos = json.loads(contenido)
                    if isinstance(datos, dict) and not datos:
                        # Si el archivo contiene un diccionario vacío, eliminarlo
                        os.remove(ruta_archivo)
                except json.JSONDecodeError:
                    pass

def calcular_cuadrado(num_blocks_merge):
    final=0

    while(2**final<num_blocks_merge):
        final+=1

    return final

def save_block(nombre_carpeta,num_block,bloque):
        # Nombre del archivo dentro de la carpeta
        nombre_archivo = 'block' + str(num_block) + '.json'

        # Combinar la carpeta y el nombre de archivo para obtener la ruta completa
        ruta_completa = os.path.join(nombre_carpeta, nombre_archivo)

        # Asegúrate de que la carpeta exista antes de guardar el archivo
        if not os.path.exists(nombre_carpeta):
            os.makedirs(nombre_carpeta)

        with open(ruta_completa, 'w',encoding="utf-8") as f:
            json.dump(bloque, f,ensure_ascii=False, indent=4)
