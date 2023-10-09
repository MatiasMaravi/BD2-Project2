import nltk
from nltk.stem.snowball import SnowballStemmer


with open("docs/stoplist.txt", encoding='latin1', ) as file:
    stoplist = [line.rstrip().lower() for line in file]
stemmer = SnowballStemmer("spanish")
def preprocesamiento(texto) -> list:
    return [stemmer.stem(word.lower()) for word in nltk.word_tokenize(texto) if word.isalpha() and word.lower() not in stoplist]