# Preprocesamiento


- El preprocesamiento de textos es una fase crucial para garantizar la calidad y eficacia de las aplicaciones de procesamiento de texto, ya que permite convertir datos textuales crudos en información estructurada y procesable.
## Pasos


### 1. Tokenización
- En este paso se divide el texto en unidades más pequeñas llamadas “tokens”. Es esencial para facilitar el análisis y procesamiento de texto o tareas posteriores al preprocesamiento.


### 2.Eliminar signos innecesarios


-  En este paso se eliminan los signos de puntuación y caracteres especiales encontrados en el texto.


### 3. Filtrar StopWords
- En este paso se debe utilizar un stoplist, el cual nos ayudará a filtrar los Stopwords, los cuales son palabras consideradas muy comunes, y esto dependerá del idioma en que este escrito es texto.


### 4. Stemming


- En este paso se reemplaza cada palabra por su raíz, de tal manera que la información de cada palabra no se pierda por completo pero se eliminen sus prefijos o sufijos. De esta manera se simplifican las palabras derivadas.




## Implementación

- Importamos las librerias para realizar el preprocesamiento

``` python
import nltk
from nltk.stem.snowball import SnowballStemmer

```
- Abrimos el archivo que contiene los Stopwords, luego eliminamos cualquier espacio en blanco y se convierte cada palabra a minuscula. El resultado es una lista de palabras en minúsculas que se consideran stopwords.

``` python
with open("assets/resources/stoplist.txt", encoding='latin1', ) as file:
stoplist = [line.rstrip().lower() for line in file]
```
- Inicializamos el Stemmer. El lenguaje dependera de los textos, en este caso elegimos ingles, ya que la base de datos que da origen a los textos estan en ingles.

``` python
stemmer = SnowballStemmer("english")
```

- Definimos la funcion `preprocesamiento(texto)` la cual recibe el texto a preprocesar y retorna el texto procesado. En resumen esta funcion limpia, tokeniza, aplica el stemming y elimina las stopwords, produciendo una lista de palabras preprocesadas que pueden ser utilizadas en análisis posteriores, como análisis de texto o minería de información.

``` python
def preprocesamiento(texto) -> list:
    return [stemmer.stem(word.lower()) for word in nltk.word_tokenize(texto) if word.isalpha() and word.lower() not in stoplist]
```