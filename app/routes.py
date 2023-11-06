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

    consulta_str = str(consulta)
    topk_int = int(topk)

    sql_query = f'''
        SELECT track_name,playlist_name, track_artist,ts_rank(content_idx, query) as rank 
        FROM spotify_songs, to_tsquery('english', '{consulta_str}') query 
        WHERE content_idx @@ query 
        ORDER BY rank DESC 
        LIMIT {topk_int};
    '''

    resultados, tiempo_ejecucion = run_query(sql_query)

    # Construye una lista de resultados en un formato adecuado para JSON
    resultados_json = [{'track_name': resultado[0], 'playlist_name': resultado[1],'track_artist': resultado[2], 'rank': resultado[3]} for resultado in resultados]
    print(resultados_json)

    return jsonify({'tiempo_ejecucion': tiempo_ejecucion, 'resultados': resultados_json})


