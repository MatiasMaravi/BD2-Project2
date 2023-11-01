# Instalacion de MongoDB en Macos

Homebrew requiere las herramientas de línea de comandos Xcode de Xcode de Apple.
Requisitos:
* Instalar xcode
```
xcode-select --install
```
* Instalar homebrew
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Para descargar la fórmula oficial de Homebrew para MongoDB y las herramientas de base de datos, ejecutando el siguiente comando en su terminal macOS:
```
brew tap mongodb/brew
```

* Actualizar homebrew
```
brew update
```

* Instalar mongodb
```
brew install mongodb-community@7.0
```

Para ejecutar MongoDB realizar lo siguiente
```
brew services start mongodb-community@7.0
```
y luego iniciamos.
```
mongosh
```
# Creamos nuestra base de datos

Realizamos el comando:

```
use BasedeDatosProyect2
```

Para popular y rellenar de datos nuestra base de datos usaremos un bucle for en dos campos del tipo string en cada uno de ellos con la cantidad pedida:

```
const numDocuments = [1000, 2000, 4000, 8000, 16000, 32000,64000];

for (const num of numDocuments) {
  const collectionName = `miColeccion${num}`;
  db.createCollection(collectionName);

  const documents = [];

  for (let i = 1; i <= num; i++) {
    documents.push({ campo1: `valor1_${i}`, campo2: `valor2_${i}` });
  }

  db[collectionName].insertMany(documents);
}
```
Verificamos la colecciones esten pobladas con:
```
show collections
```



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
