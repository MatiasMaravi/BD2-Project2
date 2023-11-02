from flask import render_template, request, jsonify
from app import app
from main import mostrar,get_db,run_query

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/mostrar_indice', methods=['POST'])
def calcular_distancia_route():

    consulta = request.form.get('consult_i')
    topk = request.form.get('topk')

    # Asegúrate de que los valores estén en el formato adecuado (pueden requerir conversión)
    consulta_str = str(consulta)
    topk_int = int(topk)

    # Construye la consulta SQL con los valores de consulta y topk
    sql_query = f'''
        SELECT track_name, ts_rank(content_idx, to_tsquery('english', '{consulta_str}')) as rank
        FROM spotify_songs, to_tsquery('english', '{consulta_str}') query
        WHERE content_idx @@ query
        ORDER BY rank DESC
        LIMIT {topk_int};
    '''

    resultados, tiempo_ejecucion = run_query(sql_query)

    # print("Resultados de la consulta:", resultados)
    print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")

    #distancia = mostrar()

    return jsonify({'Tiempo de ejecucion': tiempo_ejecucion})


