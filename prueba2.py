import tempfile
import json
import psutil

collection = [
    "doc/doc1.txt",
    "doc/doc2.txt",
    "doc/doc3.txt",
    "doc/doc4.txt",
    "doc/doc5.txt"
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

initialRam = psutil.virtual_memory().available

inverted_index = BSBindexConstrucction()

# Mostrar el índice invertido en formato JSON
print(json.dumps(inverted_index, indent=4))
with open("json-data.json", "w") as file:
   json.dump(inverted_index, file)

finalRam = psutil.virtual_memory().available

print("Initial Ram:", initialRam)
print("Final RAM:", finalRam)
print("Difference RAM:", initialRam - finalRam)