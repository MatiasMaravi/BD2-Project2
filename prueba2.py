import tempfile
import json

collection = [
    "/Users/pierre/Documents/5-ciclo/BaseDeDatosII/BD2-Project2/doc/doc1.txt",
    "/Users/pierre/Documents/5-ciclo/BaseDeDatosII/BD2-Project2/doc/doc2.txt",
    "/Users/pierre/Documents/5-ciclo/BaseDeDatosII/BD2-Project2/doc/doc3.txt",
    "/Users/pierre/Documents/5-ciclo/BaseDeDatosII/BD2-Project2/doc/doc4.txt",
    "/Users/pierre/Documents/5-ciclo/BaseDeDatosII/BD2-Project2/doc/doc5.txt"
]

def BSBindexConstrucction():
    n = 0
    inverted_index = {}

    while not all_documents_processed():
        n = n + 1
        document = get_current_document()
        tokenstream = parse_document(document)
        if tokenstream is not None:
            update_inverted_index(inverted_index, tokenstream, document)

    return inverted_index

def update_inverted_index(inverted_index, tokenstream, document):
    for token in tokenstream:
        if token not in inverted_index:
            inverted_index[token] = {
                "frequency": 1,
                "documents": [document]
            }
        else:
            inverted_index[token]["frequency"] += 1
            if document not in inverted_index[token]["documents"]:
                inverted_index[token]["documents"].append(document)

def all_documents_processed():
    return not collection

def get_current_document():
    if not collection:
        return None
    return collection.pop()

def parse_document(document):
    if document is None:
        return None
    with open(document, 'r') as file:
        for line in file:
            for token in line.split():
                yield token

inverted_index = BSBindexConstrucction()

# Mostrar el índice invertido en formato JSON
print(json.dumps(inverted_index, indent=4))

