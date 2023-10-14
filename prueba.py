import tempfile

collection = ["doc1.txt", "doc2.txt", "doc3.txt", "doc4.txt", "doc5.txt"]

def all_documents_processed():
    return not collection

def ParseDocs():
    if not collection:
        return None

    # Obtener el próximo documento en la colección.
    current_document = collection.pop(0)
    
    # Leer el contenido del documento y dividirlo en palabras.
    with open(current_document, 'r') as doc_file:
        document_content = doc_file.read()
        words = document_content.split()

    return words

def BSBINDEXCONSTRUCTION():
    n = 0
    merge_output_files = []

    while not all_documents_processed():
        n = n + 1
        token_stream = ParseDocs()
        if token_stream is not None:
            output_file = SPIMI_invert(token_stream)
            merge_output_files.append(output_file)

    final_index = merge(merge_output_files)

    return final_index

def SPIMI_invert(token_stream):
    output_file = tempfile.NamedTemporaryFile(delete=False)
    dictionary = {}

    for token in token_stream:
        if token not in dictionary:
            dictionary[token] = [1, [token]]
        else:
            dictionary[token][0] = dictionary[token][0] + 1

    for key in sorted(dictionary.keys()):
        postings_list = dictionary[key]
        postings_list[1].sort()
        postings = ','.join(str(x) for x in postings_list[1])
        output_file.write(key + ':' + str(postings_list[0]) + ':' + postings + '\n')

    output_file.seek(0)
    return output_file

def merge(files):
    output_file = tempfile.NamedTemporaryFile(delete=False)
    dictionary = {}
    files = [open(file.name, 'r') for file in files]

    for file in files:
        line = file.readline()
        if line != '':
            key = line.split(':')[0]
            if key not in dictionary:
                dictionary[key] = [line]
            else:
                dictionary[key].append(line)

    while len(dictionary) > 0:
        min_key = min(dictionary.keys())
        min_list = dictionary[min_key]
        output_file.write(min_list.pop(0))

        if len(min_list) == 0:
            del dictionary[min_key]
        else:
            dictionary[min_key] = min_list

    output_file.seek(0)
    return output_file

# Llamar a la función BSBINDEXCONSTRUCTION para construir el índice invertido.
final_index = BSBINDEXCONSTRUCTION()

# Imprimir el índice invertido final.
with open(final_index.name, 'r') as index_file:
    index_content = index_file.read()
    print("Índice Invertido Final:")
    print(index_content)

# Cerrar y eliminar archivos temporales.
final_index.close()

