from flask import render_template, request, jsonify
from app import app
from main import get_db,run_query

@app.route('/')
def index():
    return render_template('index.html')





@app.route('/mostrar_indice', methods=['POST'])
def calcular_distancia_route():

    consulta = request.form.get('consulta_i')
    topk = request.form.get('topk')
    language = request.form.get('language')




    consulta_str = str(consulta)
    topk_int = int(topk)
    language_str = str(language)

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


    # Construye una lista de resultados en un formato adecuado para JSON
    resultados_json = [{'track_name': resultado[0], 'playlist_name': resultado[1],'track_artist': resultado[2], 'rank': resultado[3]} for resultado in resultados]
    print(resultados_json)

    return jsonify({'tiempo_ejecucion': tiempo_ejecucion, 'resultados': resultados_json})


