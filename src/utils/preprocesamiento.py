import nltk
from nltk.stem.snowball import SnowballStemmer



def preprocesamiento(texto) -> list:
    with open("assets/resources/stoplist.txt",encoding='utf-8') as file:
        stoplist = [line.rstrip().lower() for line in file]
    stemmer = SnowballStemmer("english")
    return [stemmer.stem(word.lower()) for word in nltk.word_tokenize(texto) if word.isalpha() and word.lower() not in stoplist]
