import nltk
from nltk.stem.snowball import SnowballStemmer


with open("stoplist.txt", encoding='latin1', ) as file:
    stoplist = [line.rstrip().lower() for line in file]

def preprocesamiento(texto):
  # Tokenizar
    tokens = nltk.word_tokenize(texto)
    tokens = [word.lower() for word in tokens if word.isalpha()] #Lo volvemos minuscula
  # filtrar stopwords
    tokens = [word for word in tokens if word.lower() not in stoplist]
  # reducir palabras
    stemmer = SnowballStemmer("spanish")
    tokens = [stemmer.stem(word) for word in tokens]

    return tokens
