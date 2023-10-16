# Indexacion en MongoDB

MongoBD para le recuperacion de informacion, utiliza un indice especializado en campos de tipo texto, a este se le conoce como `indice de texto`.

Este indice para la recuperacion eficiente de informacion, utiliza una tecnica llamada `inverted index` o `indice invertido`, que consiste en un diccionario que mapea palabras a documentos, a la que asigna pesos que representan la importancia de la palabra en el documento.

## Indice invertido

El indice invetido en MongoDB, funciona de la siguiente manera:

1. Se tokeniza el texto, es decir, se separa en palabras.
2. Se eliminan las palabras vacias, como articulos, preposiciones, etc.
3. Cada token se almacena en el indice, junto con una referencia del documento en el que aparece.
4. Se calcula el peso de cada token en cada documento, y se almacena en el indice.
5. Para realizar una consulta de texto completo se utiliza el operador `$text`, que recibe como parametro la consulta, y devuelve los documentos que contienen las palabras de la consulta, ordenados por relevancia.
6. MongoDB utiliza el algoritmo `TF-IDF` para calcular la relevancia de cada documento.

  ### Ejemplo de uso

 - Creamos un índice de texto en un campo llamado "descripcion" en una colección  llamada "productos":
  ```python
    db.productos.createIndex({ descripcion: "text" });
  ```
  - Para realizar una consulta de texto completo, utilizamos el operador `$text`, en este caso, buscamos los documentos que contienen la palabra "pantalon" en el campo "descripcion":
  ```python
    db.productos.find({ $text: { $search: "pantalon" } });
  ```