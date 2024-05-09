from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('inicio.html')


@app.route('/partidos', methods=['GET', 'POST'])
def partidos():
    if request.method == 'POST':
        partido_numero = request.form['partido_numero']
        resultados = obtener_partidos(partido_numero)
        if not resultados:
            mensaje = f"No se encontraron partidos para el número {partido_numero}."
            return render_template('partidos.html', mensaje=mensaje)
        return render_template('partidos.html', resultados=resultados)
    return render_template('partidos.html')


def obtener_partidos(partido_numero):
    url = f'https://api.football-data.org/v4/matches/{partido_numero}/head2head'
    token = os.environ.get('token')
    headers = {'X-Auth-Token': token}
    response = requests.get(url, headers=headers)
    datos = response.json()

    resultados = []
    if response.status_code == 200:
        for match in datos['matches']:
            fecha = match['utcDate']
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            competicion = match['competition']['name']
            imagen_comp = match['competition']['emblem']
            escudo_local = match['homeTeam']['crest']
            escudo_visit = match['awayTeam']['crest']
            goles_local = match['score']['fullTime']['home']
            goles_visit = match['score']['fullTime']['away']

            numero_partido = match['id']  
            resultado_partido = {
                'fecha': fecha,
                'local': home_team,
                'visitante': away_team,
                'numero_partido': numero_partido,
                'competicion': competicion,
                'imagen_comp': imagen_comp,
                'escudo_local': escudo_local,
                'escudo_visit': escudo_visit,
                'goles_local': goles_local,
                'goles_visit': goles_visit
            }

            resultados.append(resultado_partido)
    return resultados



@app.route('/detalle_partido/<int:partido_numero>')
def detalles_partido(partido_numero):
    resultados = obtener_partidos(partido_numero)
    if not resultados:
        mensaje = f"No se encontró un partido con el número {partido_numero}."
        return render_template('detalle_partido.html', mensaje=mensaje)
    
    # Buscamos el partido correspondiente al número de partido seleccionado
    partido_seleccionado = None
    for partido in resultados:
        if partido['numero_partido'] == partido_numero:
            partido_seleccionado = partido
            break
    
    # Si no se encontró el partido, mostramos un mensaje de error
    if not partido_seleccionado:
        mensaje = f"No se encontró un partido con el número {partido_numero}."
        return render_template('detalle_partido.html', mensaje=mensaje)
    
    # Pasamos las variables del partido seleccionado a la plantilla
    return render_template('detalle_partido.html',goles_local = partido_seleccionado['goles_local'],goles_visit = partido_seleccionado['goles_visit'] ,escudo_local = partido_seleccionado['escudo_local'], escudo_visit= partido_seleccionado['escudo_visit'], imagen_comp = partido_seleccionado['imagen_comp'],competicion = partido_seleccionado['competicion'], fecha=partido_seleccionado['fecha'], local=partido_seleccionado['local'], visitante=partido_seleccionado['visitante'])








if __name__ == '__main__':
    app.run(debug=True)
