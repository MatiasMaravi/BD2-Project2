# Indice Invertido

- El inidice invertido es una tecnica utilizada en la recuperacion de informacion y de la busqueda de texto, ademas permite una búsqueda eficiente de palabras clave en grandes cantidades de texto.

## Implementación

- Implementamos la clase `InvertIndex` la cual tiene como atributos el archivo de indice, el indice, el idf y la longitud de los documentos.

``` python
class InvertIndex: 

    def __init__(self, index_file):
        self.index_file = index_file
        self.index = {}
        self.idf = {}
        self.length = {}
```
- En el funcion `load_index()` cargamos el indice invertido desde el archivo de indice el cual esta en formato json.

``` python
    def load_index(self, index_file):
        try:
            with open(index_file, 'r') as f:
                data = json.load(f)
                self.index = data['index']
                self.idf = data['idf']
                self.length = data['length']
        except FileNotFoundError:
            print("El archivo de índice no existe. Debe construirlo primero usando la función `building`.") 
```

- En la funcion `building()` construimos el indice invertido a partir de los documentos que se encuentran en la carpeta `docs` y lo guardamos en el archivo `index.json`, esto lo realizamos con el proposito de evitar recalculos al momento de querer usar el indice invertido , es decir, lo calculamos una vez y lo guardamos para una futura utilizacion del mismo, ademas que si el indice invertido es muy grande no se podria tener en memoria principal `(RAM)`, por ello se lleva a memoria secundaria.

``` python
    def building(self, collection_text):
        # build the inverted index with the collection
        textos_procesados = []
        
        for file_name in collection_text:
            file = open(file_name)
            texto = file.read().rstrip()
            texto = preprocesamiento(texto)  
            textos_procesados.append(texto) 

        # compute the tf
        self.index=tf_dic(tf(textos_procesados,collection_text))

        # compute the idf
        self.idf=idf_dic(df(textos_procesados),len(textos_procesados))
    
        # compute the length (norm)
        
        #self.length=norm(textos_procesados,collection_text)
        self.length=norma(self.index,self.idf,collection_text)         

        # store in disk
        data = {
            'index': self.index,
            'idf': self.idf,
            'length': self.length
        }
        with open(self.index_file, 'w') as f:
            json.dump(data, f)
```

- En la función `retriveral()` hallamos la similitud coseno a partir de los diccionarios de los pesos tf y idf, en donde iteramos a travez los keywords de la query y buscamos los concidentes con cada documento de la coleccion, luego calculamos el peso tf-idf y asignamos el `score` correspondiente a cada documento.

``` python
def retrieval(self, query, k):
        self.load_index(self.index_file)

        # diccionario para el score
        score = {}

        # preprocesar la query: extraer los terminos unicos
        queryPrep = preprocesamiento(query)

        # aplicar similitud de coseno y guardarlo en el diccionario score
        for key in self.length.keys():
            score[key] = 0

        query_term_unic=set(queryPrep)

        lenght_query=[]

        for term in query_term_unic:
            # Validamos si existe el término en nuestros diccionarios
            if term not in self.idf and term not in self.index:
                continue

            # calcular el tf-idf del query
            term_tf = math.log10(1+queryPrep.count(term))
            
            term_idf = self.idf[term]
            term_doc = self.index[term]
            
            lenght_query.append(term_tf*term_idf)

            for doc in term_doc:
                score[doc] += self.index[term][doc]*term_idf*term_tf*term_idf

        norma_query=np.linalg.norm(np.array(lenght_query))

        for doc in score:
            score[doc] /= (self.length[doc]*norma_query)  
            score[doc] = round(score[doc], 2)      

            
        # ordenar el score de forma descendente
        result = sorted(score.items(), key= lambda tup: tup[1], reverse=True)
        # retornamos los k documentos mas relevantes (de mayor similitud al query)
        return result[:k]

```


- Como funciones externas a la clase `InvertIndex` tenemos las siguientes:

  - `tf()` la cual calcula el tf de cada palabra en cada documento, es decir la frecuencia de cada palabra en cada documento.

    ``` python
    def tf(books,textos):
        frecuencia = {}
        tokens = []
        #1. Crear una lista de tokens general
        for i in books:
            tokens+=i

        tokens=set(tokens)

        #2. Crear la matriz de frecuencias de cada documento
        for i,libro in enumerate(books):

            tokens_libro = libro

            for token in tokens:
                if token not in frecuencia:
                    frecuencia[token] = {textos[i]: 0}
                else:
                    frecuencia[token][textos[i]] = 0

            for token_libro in tokens_libro:
                if token_libro in frecuencia:
                    frecuencia[token_libro][textos[i]] += 1

        frecuencia= dict(sorted(frecuencia.items()))           
                
        return frecuencia
    ```
  - `tf_dic()` es esta funcion normalizamos los pesos tf de cada palabra en cada documento,esto lo realizamos aplicando la funcion `math.log10()`, la cual calcula el logaritmo en base 10.

    ``` python
    def tf_dic(tf):
        #np.log10(1 + np.array([[TF[token]['libro'+ str(i+1)] for token in TF] for i,book in enumerate(collection)]))
        for token in tf:
            for book in tf[token]:
                tf[token][book]=math.log10(1+ tf[token][book])
        return tf  
    ```     

  - `df()` la cual calcula el df de cada palabra, es decir la cantidad de documentos en los que aparece cada palabra.

    ``` python
    def df(books):

        pesos={}

        for i in books:
            lista=set(i)
            for j in lista:
                if j not in pesos:
                    pesos[j]=1
                else:
                    pesos[j]+=1

        pesos=dict(sorted(pesos.items()))            
        return pesos 
    ```
  - `idf_dic()` en esta funcion hallamos el peso idf de cada palabra, asi como tambien la normalizacion la cual realizamos a travez de la funcion `math.log10()`.

    ``` python
    def idf_dic(df,num_textos):
        #IDF = np.log10(len(collection)/np.array([DF[token] for token in DF]))
        for token in df:
            df[token]=math.log10(num_textos/df[token])

        return df
    ```

  - `norma()` en esta funcion hallamos la norma de un documento, la cual consiste en la raiz cuadrada de la sumatoria de los cuadrados de cada valor de frecuencia de los terminos de un documento, esto lo determinamos de manera mas simplificada con la funcion `np.lialg.norm`.

     ![Alt text](image.png)


    ``` python
    # La norma se saca a partir de los pesos tf-idf
    def norma(tf,idf,collection_text):
        length={}
        TF = np.array([[tf[token][textos[i]] for token in tf] for i,tokens in enumerate(collection_text)])
        IDF = np.array([idf[token] for token in idf])
        
        TF_IDF=TF*IDF

        for i,book in enumerate(collection_text):
            length[book]=np.linalg.norm(TF_IDF[i])

        return length
    ```  
