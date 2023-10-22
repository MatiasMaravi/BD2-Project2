from flask import render_template, request, jsonify
from app import app
from main import mostrar

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mostrar_indice', methods=['POST'])
def calcular_distancia_route():
    city1 = request.form.get('city1')

    city2 = request.form.get('city2')
    country2 = request.form.get('country2')
    metodo = request.form.get('metodo')

    distancia = mostrar()

    return jsonify({'distancia': distancia})
