import nltk
# nltk.download('stopwords') Necesario al ejecutar por primera vez
# nltk.download('punkt') Necesario al ejecutar por primera vez
from nltk.stem.snowball import SnowballStemmer



def preprocesamiento(texto,idioma) -> list:
    if idioma == 'es':
        with open("assets/resources/stoplist.txt",encoding='utf-8') as file:
            stoplist = [line.rstrip().lower() for line in file]
        stemmer = SnowballStemmer("spanish")
        return [stemmer.stem(word.lower()) for word in nltk.word_tokenize(texto) if word.isalpha() and word.lower() not in stoplist]
    elif idioma == 'en':
        #usamos la libreria nltk para descargar el stoplist en ingles
        
        from nltk.corpus import stopwords
        stoplist = stopwords.words('english')
        stemmer = SnowballStemmer("english")
        return [stemmer.stem(word.lower()) for word in nltk.word_tokenize(texto) if word.isalpha() and word.lower() not in stoplist]

