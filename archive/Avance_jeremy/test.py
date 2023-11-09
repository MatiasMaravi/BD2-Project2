import psutil
import sys
import json
import nltk
import os
import numpy as np
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
nltk.download('punkt')

collection = [
    "doc/doc1.txt",
    "doc/doc2.txt",
    "doc/doc3.txt",
    "doc/doc4.txt",
    "doc/doc5.txt"
]


def allDocumentsProcessed(collection: list):
    # Retorna True si la lista está vacía
    return not collection


def getCurrentDoc (collection: list):
    # Retorna el último valor de la lista
    return collection.pop()


def parseDoc (document: str):
    with open("stoplist.txt", encoding='latin1') as file:
        stoplist = [line.rstrip().lower() for line in file]
    
    doc_id = os.path.basename(document).split('.')[0]
    
    # Obtener el texto del documento
    with open(document, 'r', encoding='utf-8') as document:
        texto = document.read()
    
    # Tokenizar
    tokens = []
    tk = RegexpTokenizer(r'\w+')
    tokens = tk.tokenize(texto.lower())

    # Filtrar stopwords
    tokens = [word for word in tokens if word not in stoplist]

    # Reducir palabras
    snowStemmer = SnowballStemmer(language='spanish')
    for i in range (0, len(tokens)):
        tokens[i] = snowStemmer.stem(tokens[i])
    #Devolvemos una lista de tuplas (termino,doc_id) como dice la linea 4     
    term_doc_tuples = [(term, doc_id) for term in tokens]
    
    return term_doc_tuples


def SPIMI_Invert (tokenStream: list):
    outputFile = "outputFile.json"
    dictionary = dict()

    initialRam = psutil.virtual_memory().available
    usedRam = -1
    print(f"{tokenStream} y tamaño {len(tokenStream)}")
    
    while usedRam != 0 and tokenStream:
        currentRam = psutil.virtual_memory().available
        usedRam = initialRam - currentRam
        
        token = tokenStream.pop()
        postingsList = np.full(10,-1)
        
        if token not in dictionary:
            postingsList = addToDict(dictionary, token[0])
        else:
            postingsList = getPostingsList(dictionary, token[0])
        
        if full(postingsList):
           postingsList = doublePostingsList(dictionary, token)
        
        addToPostingsList(postingsList, docID(token))
        
    sT = dict(sorted(dictionary.items()))
    print(f"Lista ordenada \n{sT} y tamaño {len(sT)}")
    
    writeBlockFile(sT, dictionary, outputFile)
    
    return outputFile

def getPostingsList(dictionary: dict, token: str):
    return dictionary[token]

def addToDict(dictionary: dict, token: str):
    dictionary[token] = list()
    return dictionary[token]

def addToPostingsList(postingsList: list, docID: int):
    if docID not in postingsList:
        postingsList.append(docID)
    return postingsList

def docID(token : str):
    return int(token[1][-1])

def doublePostingsList(dictionary: dict, token: str):
    postingsList = getPostingsList(dictionary, token[0])
    postingsList = np.concatenate((postingsList, np.full(10,-1)))
    return postingsList

def full(postingsList: list):
    #Para saber si usamos solo 20 mb cambiar a la memoria que vamos usar
    if memoria_usada(tamanhio_array_bytes(postingsList),20):
        return True
    else:
        return False


def tamanhio_array_bytes(array):
    if len(array) == 0:
        return 0
    tamanhios_bytes = [sys.getsizeof(i) for i in array]
    tamanhio_prom = sum(tamanhios_bytes)
    return tamanhio_prom

def memoria_usada(tamanhio,n):
    tamanhio_megabytes = tamanhio / (1024*1024)
    if tamanhio_megabytes > n:
        return True
    else:
        return False

def writeBlockFile(sT: dict, dictionary: dict, outputFile: str):
    with open(outputFile, 'w', encoding='utf-8') as file:
        json.dump(sT, file, ensure_ascii=False, indent=4)

def mergeBlocks(files: list, mergedFile: str):
    with open(mergedFile, 'w', encoding='utf-8') as file:
        for f in files:
            with open(f, 'r', encoding='utf-8') as block:
                data = json.load(block)
                json.dump(data, file, ensure_ascii=False, indent=4)
    return mergedFile
def BSBIndexConstruction (collection: list):
    files = list()
    mergedFile = "mergedFile.json"
    while not allDocumentsProcessed(collection):
        document = getCurrentDoc(collection)
        tokenStream = parseDoc(document)
        nFile = SPIMI_Invert(tokenStream)
        files.append(nFile)

    return mergeBlocks(files, mergedFile)
print(BSBIndexConstruction(collection))
