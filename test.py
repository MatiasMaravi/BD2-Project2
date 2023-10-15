import psutil
import json

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

def BSBIndexConstruction (collection: list):
    files = list()
    mergedFile = "mergedFile.json"

    while not allDocumentsProcessed(collection):
        document = getCurrentDoc(collection)
        tokenStream = parseDoc(document)
        nFile = SPIMI_Invert(tokenStream)
        files.append(nFile)

    return MergeBlocks(files, mergedFile)

def allDocumentsProcessed (collection: list):
    # Retorna True si la lista está vacía
    return not collection

def getCurrentDoc (collection: list):
    # Retorna el último valor de la lista
    return collection.pop()

def SPIMI_Invert (tokenStream):
    return False
