def merge_sort_dicts(dict1, dict2):
    # Obtenemos las claves de ambos diccionarios
    keys1 = list(dict1.keys())
    keys2 = list(dict2.keys())

    # Aplicamos Merge Sort a las claves
    sorted_keys = merge(keys1, keys2)

    # Creamos un nuevo diccionario ordenado
    sorted_dict = {}

    for key in sorted_keys:
        if key in dict1 and key in dict2:
            sorted_dict[key] = [dict1[key], dict2[key]]
        elif key in dict1:
            sorted_dict[key] = [dict1[key]]
        else:
            sorted_dict[key] = [dict2[key]]

    return sorted_dict

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


# Ejemplo de uso:
dict1 = {'apple': 3, 'banana': 2, 'cherry': 5, 'mandarina': 1, 'grape': 4}
dict2 = {'date': 1, 'grape': 4, 'apple': 6,}

sorted_dict = merge_sort_dicts(dict1, dict2)
print(sorted_dict)

dicion={}
print(len(dicion))
