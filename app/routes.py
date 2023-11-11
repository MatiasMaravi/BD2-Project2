from flask import render_template, request, jsonify
from app import app
from main import get_db,run_query
from pymongo import MongoClient
from bson import ObjectId
import json
import time


def jsonify_with_objectid_support(obj):
    """JSONify object with support for ObjectId."""
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj


client = MongoClient('mongodb://localhost:27017/')  # Cambia la URL según tu configuración
db = client['BasedeDatosProyect2']  # Cambia al nombre de tu base de datos
collection = db['spotify_songs']

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/consulta', methods=['GET'])
def consulta():
    # Realizar la consulta en MongoDB
    resultado = collection.find(
        {"$text": {"$search": "Holy"}},
        {"score": {"$meta": "textScore"}, "track_name": 1, "playlist_name": 1, "track_artist": 1}
    ).sort([("score", {"$meta": "textScore"})]).limit(10)

    resultados_lista = [json.loads(json.dumps(resultado_item, default=jsonify_with_objectid_support)) for resultado_item
                        in resultado]

    # Retornar los resultados como JSON
    return jsonify(resultados_lista)

@app.route('/mostrar_indice', methods=['POST'])
def calcular_distancia_route():

    consulta = request.form.get('consulta_i')
    topk = request.form.get('topk')
    language = request.form.get('language')
    metodo = request.form.get('metodo')


    consulta_str = str(consulta)
    topk_int = int(topk)
    language_str = str(language)
    metodo_str = str(metodo)

    print(metodo_str)

    if metodo_str == "postgres":

        lista = consulta_str.split(" ")
        frase = ""
        i = 0
        if len(lista) > 1:
            for i in range(len(lista)):
                if i == 0:
                    frase += lista[i]
                else:
                    frase += " & "
                    frase += lista[i]
                i += 1
        else:
            frase = consulta_str

        sql_query = ""

        if language_str == "spanish":
            sql_query = '''
                SELECT track_name,playlist_name, track_artist,ts_rank(content_idx, query) as rank 
                FROM spotify_es, to_tsquery('spanish', %s) query 
                WHERE content_idx @@ query 
                ORDER BY rank DESC 
                LIMIT %s;
            '''

        elif language_str == "english":
            sql_query = '''
                SELECT track_name,playlist_name, track_artist,ts_rank(content_idx, query) as rank 
                FROM spotify_en, to_tsquery('english', %s) query 
                WHERE content_idx @@ query 
                ORDER BY rank DESC 
                LIMIT %s;
            '''
        resultados, tiempo_ejecucion = run_query(sql_query, frase, topk_int)

        resultados_json = [{'track_name': resultado[0], 'playlist_name': resultado[1],'track_artist': resultado[2], 'rank': resultado[3]} for resultado in resultados]


        return jsonify({'tiempo_ejecucion': tiempo_ejecucion, 'resultados': resultados_json})



    elif metodo_str == "mongodb":

        start_time = time.time()  # Registra el tiempo de inicio

        resultado = collection.find(
            {"$text": {"$search": consulta_str}},
            {"score": {"$meta": "textScore"}, "track_name": 1,"playlist_name":1, "track_artist": 1}
        ).sort([("score", {"$meta": "textScore"})]).limit(topk_int)

        end_time = time.time()

        execution_time = end_time - start_time

        resultados_lista = [
            {
                'track_name': resultado_item['track_name'],
                'playlist_name':resultado_item['playlist_name'],
                'track_artist': resultado_item['track_artist'],
                'rank': resultado_item['score']
            } for resultado_item in resultado
        ]

        # Agrega el tiempo de ejecución a los resultados
        resultados_json = {'tiempo_ejecucion': execution_time, 'resultados': resultados_lista}
        print(resultados_json)

        # Retornar los resultados como JSON
        return jsonify(resultados_json)
    else:



        return jsonify({'error': 'Método no válido'})





