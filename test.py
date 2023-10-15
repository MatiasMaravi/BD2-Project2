import psutil
import json
import nltk
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

def BSBIndexConstruction (collection: list):
    files = list()
    mergedFile = "mergedFile.json"

    while not allDocumentsProcessed(collection):
        document = getCurrentDoc(collection)
        tokenStream = parseDoc(document)
        nFile = SPIMI_Invert(tokenStream)
        files.append(nFile)

    return mergeBlocks(files, mergedFile)

def allDocumentsProcessed (collection: list):
    # Retorna True si la lista está vacía
    return not collection

def getCurrentDoc (collection: list):
    # Retorna el último valor de la lista
    return collection.pop()

def parseDoc (document: str):
    with open("stoplist.txt", encoding='latin1') as file:
        stoplist = [line.rstrip().lower() for line in file]
    
    # Obtener el texto del documento
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
    
    return tokens

def SPIMI_Invert (tokenStream: list):
    outputFile = "outputFile.json"
    dictionary = dict()

    initialRam = psutil.virtual_memory().available
    usedRam = -1

    while usedRam != 0 and tokenStream:
        currentRam = psutil.virtual_memory().available
        usedRam = initialRam - currentRam
        
        token = tokenStream.pop()
        
        if token not in dictionary:
            postingsList = addToDict(dictionary, token)
        else:
            postingsList = getPostingsList(dictionary, token)
        
        if full(postingsList):
            postingsList = doublePostingsList(dictionary, token)
        
        addToPostingsList(postingsList, docID(token))
    
    sT = sortedTerms(dictionary)
    writeBlockFile(sT, dictionary, outputFile)

    return outputFile


def getPostingsList(dictionary: dict, token: str):
    return dictionary[token]

def addToDict(dictionary: dict, token: str):
    dictionary[token] = list()
    return dictionary[token]

def addToPostingsList(postingsList: list, docID: int):
    pass
