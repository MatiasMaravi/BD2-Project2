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
Consultas sin indices en todas las colecciones:

```
const startTime = Date.now();

//Donde N es la cantidad de values por coleccion.
const result = db.miColeccionN.find({ campo1: `valor1_9` });

const endTime = Date.now();

const executionTime = endTime - startTime;

printjson(result);
print(`Tiempo de ejecución: ${executionTime} ms`);
```

Coleccion de 1000:

<img width="1210" alt="Captura de pantalla 2023-11-01 a la(s) 10 33 44" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/9af3eba8-7368-4a23-8c5f-e1bcab01238e">
Tiempo de ejecución es 48 ms.

Coleccion de 2000:

<img width="1204" alt="Captura de pantalla 2023-11-01 a la(s) 10 35 59" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/b789252d-2244-4801-a3be-7781eca7a3bf">

Tiempo de ejecución: 42 ms

Coleccion de 4000:

<img width="1191" alt="Captura de pantalla 2023-11-01 a la(s) 10 37 24" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/62ce56aa-8592-4b03-b22a-ac03777c1896">

Tiempo de ejecución: 48 ms

Coleccion de 8000:

<img width="1204" alt="Captura de pantalla 2023-11-01 a la(s) 10 38 46" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/acba957a-d7bc-4c84-accb-ba6fcdab1535">

Tiempo de ejecución: 48 ms

Coleccion de 16000:

<img width="1423" alt="Captura de pantalla 2023-11-01 a la(s) 10 40 40" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/147316c2-c471-41d1-a0d7-433ebb897dc1">

Tiempo de ejecución: 44 ms

Coleccion de 32000:
<img width="1420" alt="Captura de pantalla 2023-11-01 a la(s) 10 41 27" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/dcabd2cb-e0f2-4cdc-9a35-ecaee75e1a39">

Tiempo de ejecución: 46 ms

Coleccion de 64000:
<img width="1426" alt="Captura de pantalla 2023-11-01 a la(s) 10 42 06" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/fee0ec3f-4a41-4826-bd06-45c11aa296a2">
Tiempo de ejecución: 47 ms

En todas las colecciones en una consulta:
```
const startTime = Date.now();

const valorABuscar =  `valor1_900`;

const collectionsToSearch = [
  'miColeccion1000',
  'miColeccion2000',
  'miColeccion4000',
  'miColeccion8000',
  'miColeccion16000',
  'miColeccion32000',
  'miColeccion64000'
];

for (const collectionName of collectionsToSearch) {
  const result = db[collectionName].find({ campo1: valorABuscar });
  print(`Resultados en ${collectionName}:`);
  printjson(result);
}

const endTime = Date.now();

const executionTime = endTime - startTime;


printjson(result);
print(`Tiempo de ejecución: ${executionTime} ms`);
```
<img width="1381" alt="Captura de pantalla 2023-11-01 a la(s) 10 43 59" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/cdbe66d4-881c-496f-9295-9bb21d6d7165">
<img width="1432" alt="Captura de pantalla 2023-11-01 a la(s) 10 44 13" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/2c95faf0-e880-4ff8-a5d8-50c5ba82e7e0">
<img width="1404" alt="Captura de pantalla 2023-11-01 a la(s) 10 44 28" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/52ebd980-be36-4b74-92b5-090f2e2ea77d">
<img width="1363" alt="Captura de pantalla 2023-11-01 a la(s) 10 44 51" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/792efc4b-b8aa-4ad3-b7a4-65ecfa773f94">
<img width="1306" alt="Captura de pantalla 2023-11-01 a la(s) 10 45 02" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/1f7a2260-37da-41bb-b351-985ec6412561">
Tiempo de ejecución: 154 ms

# Indexacion en MongoDB

MongoBD para le recuperacion de informacion, utiliza un indice especializado en campos de tipo texto, a este se le conoce como `indice de texto`.

Este indice permite realizar busquedas en campos que sean cadenas o un array de elementos de cadena, actualmente existen tres versiones de este eficiente metodo de indexacion:

## Idioma por defecto
El idioma por defecto a usar es el ingles, este selecciona y determina las reglas que se utilizan para analizar las raices de las palabras (sufijo-tallo) y define las palabras de parada que se filtran. Por ejemplo, en inglés, las raíces sufijales incluyen -ing y -ed, y las palabras de parada incluyen the y a. 

## Sustitución de idioma
Especifique un nombre de campo diferente para sustituir el campo de idioma.

## Pesos de campo
Este metodo utiliza una tecnica llamada `inverted index` o `indice invertido`, MongoDB multiplica el número de coincidencias por el peso y suma los resultados. MongoDB utiliza esta suma para calcular la puntuación del documento. Seleccione un campo de la lista, especifique su peso en la casilla y haga clic en Añadir campo. El peso de campo por defecto es 1.(Esta es la version predeterminada)


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

## Experimentacion con indices
Las colecciones que tenemos anteriormente seran indexadas en el campo1, con el indice de texto.

```
const numDocuments = [1000, 2000, 4000, 8000, 16000, 32000,64000];

for (const num of numDocuments) {
  const collectionName = `miColeccion${num}`;
  const indexField =  `campo1`; 


  db[collectionName].createIndex({ [indexField]: 'text' });

  print(`Índice de texto creado en ${collectionName} para el campo ${indexField}`);
}
```
<img width="1438" alt="Captura de pantalla 2023-11-01 a la(s) 11 05 52" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/b7531312-5b53-4d82-8d95-8fcc6d20780b">

Consultas en las colecciones con MongoDB.

Coleccion de 1000 valores:

<img width="1432" alt="Captura de pantalla 2023-11-01 a la(s) 11 12 45" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/93877403-5d2c-47bb-8175-fe5125020ddc">

Tiempo de ejecución: 40 ms

Coleccion de 2000 valores:

<img width="1440" alt="Captura de pantalla 2023-11-01 a la(s) 11 13 55" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/aead33dc-ade1-4cf6-968f-b5d7a7d681c0">

Tiempo de ejecución: 39 ms

Coleccion de 4000 valores:

<img width="1440" alt="Captura de pantalla 2023-11-01 a la(s) 11 14 53" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/78db3887-d8f8-4ead-99d7-433733037680">
Tiempo de ejecución: 40 ms

Coleccion de 8000 valores:

<img width="1428" alt="Captura de pantalla 2023-11-01 a la(s) 11 15 41" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/44a1a396-48b7-4963-b6ad-5badc4bb50b0">

Tiempo de ejecución: 40 ms

Coleccion de 16000 valores:

<img width="1431" alt="Captura de pantalla 2023-11-01 a la(s) 11 17 01" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/1aa25600-98d8-4844-b67f-6feea8b0d96e">

Tiempo de ejecución: 45 ms

Coleccion de 32000 valores:

<img width="1435" alt="Captura de pantalla 2023-11-01 a la(s) 11 17 45" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/cb8135c5-3798-437f-bb1b-e5cad302a897">

Tiempo de ejecución: 42 ms

Coleccion de 64000 valores:

<img width="1438" alt="Captura de pantalla 2023-11-01 a la(s) 11 18 19" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/c348840a-daab-402c-9de1-da4a4e29417c">
Tiempo de ejecución: 43 ms

## En todas las colecciones con Indices:

```
const startTime = Date.now();

const valorABuscar =  `valor1_900`;

const collectionsToSearch = [
  'miColeccion1000',
  'miColeccion2000',
  'miColeccion4000',
  'miColeccion8000',
  'miColeccion16000',
  'miColeccion32000',
  'miColeccion64000'
];

for (const collectionName of collectionsToSearch) {
  const result = db[collectionName].find({ $text: { $search: valorABuscar } });
  print(`Resultados en ${collectionName}:`);
  printjson(result);
}

const endTime = Date.now();

const executionTime = endTime - startTime;


printjson(result);
print(`Tiempo de ejecución: ${executionTime} ms`);
```

<img width="1430" alt="Captura de pantalla 2023-11-01 a la(s) 11 20 42" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/13e1f4c7-d8ab-4ad9-9a05-a670f1f21066">
<img width="1435" alt="Captura de pantalla 2023-11-01 a la(s) 11 21 38" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/1440e396-5a36-4e73-9235-28165a8ea7d5">
<img width="1280" alt="Captura de pantalla 2023-11-01 a la(s) 11 21 53" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/c28c47d2-d030-4e49-bf4e-881390309096">
<img width="1301" alt="Captura de pantalla 2023-11-01 a la(s) 11 22 13" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/50669143-be7c-4981-96ec-3a2b123caa76">
<img width="1402" alt="Captura de pantalla 2023-11-01 a la(s) 11 22 28" src="https://github.com/MatiasMaravi/BD2-Project2/assets/91238497/75e4651c-2116-4ea2-b497-21af792744f2">
Tiempo de ejecución: 96 ms
