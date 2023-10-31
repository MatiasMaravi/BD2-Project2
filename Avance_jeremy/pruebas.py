import tempfile

collection = [
    "/Users/pierre/Documents/5-ciclo/BaseDeDatosII/BD2-Project2/doc/doc1.txt",
    "/Users/pierre/Documents/5-ciclo/BaseDeDatosII/BD2-Project2/doc/doc2.txt",
    "/Users/pierre/Documents/5-ciclo/BaseDeDatosII/BD2-Project2/doc/doc3.txt",
    "/Users/pierre/Documents/5-ciclo/BaseDeDatosII/BD2-Project2/doc/doc4.txt",
    "/Users/pierre/Documents/5-ciclo/BaseDeDatosII/BD2-Project2/doc/doc5.txt"
]

def BSBindexConstrucction():
    n = 0
    merge_output_files = []

    while not all_documents_processed():
        n = n + 1
        tokenstream = parse_document()
        if tokenstream is not None:
            outputfile = SPIMI_invert(tokenstream)
            merge_output_files.append(outputfile)

    final_index = merge(merge_output_files)

    return final_index

def SPIMI_invert(tokenstream):
    outputfile = tempfile.NamedTemporaryFile(delete=False)
    dictionary = {}

    for token in tokenstream:
        if token not in dictionary:
            dictionary[token] = [1, [token]]
        else:
            dictionary[token][0] = dictionary[token][0] + 1

    for key in sorted(dictionary.keys()):
        postings_list = dictionary[key]
        postings_list[1].sort()
        postings = ','.join(str(x) for x in postings_list[1])
        # Codifica las cadenas en bytes antes de escribirlas en el archivo
        outputfile.write(key.encode() + b':' + str(postings_list[0]).encode() + b':' + postings.encode() + b'\n')

    outputfile.seek(0)
    return outputfile

def all_documents_processed():
    return not collection

def merge(files):
    outputfile = tempfile.NamedTemporaryFile(delete=False)
    dictionary = {}
    files = [open(file.name, 'rb') for file in files]  # Abre los archivos en modo binario

    for file in files:
        line = file.readline()
        if line != b'':
            key = line.split(b':')[0].decode()  # Decodifica a cadena
            if key not in dictionary:
                dictionary[key] = [line]
            else:
                dictionary[key].append(line)

    while len(dictionary) > 0:
        min_key = min(dictionary.keys())
        min_list = dictionary[min_key]
        outputfile.write(min_list.pop(0))

        if len(min_list) == 0:
            del dictionary[min_key]
        else:
            dictionary[min_key] = min_list

    outputfile.seek(0)
    return outputfile

def parse_document():
    if not collection:
        return None
    document = collection.pop()
    with open(document, 'r') as file:
        for line in file:
            for token in line.split():
                yield token
    return document

index = BSBindexConstrucction()

# Leer y mostrar el contenido del archivo temporal
with open(index.name, 'rb') as index_file:  # Abre el archivo en modo binario
    index_content = index_file.read().decode()  # Decodifica a cadena
    print("Índice Invertido Final:")
    print(index_content)

# Cerrar y eliminar el archivo temporal
index.close()

