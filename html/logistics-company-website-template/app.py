from flask import Flask, render_template, abort, request, jsonify, session, redirect, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secretkey_here' 

@app.route('/')
def inicio():
    return render_template("inicio.html")

@app.route('/buscador')
def buscador():
    cadena = session.get('cadena_busqueda', '')  # Obtener la cadena de búsqueda de la sesión
    return render_template("buscador.html", cadena=cadena)

@app.route('/lista', methods=["GET", "POST"])
def lista():
        if request.method == "POST":
            # Obtener el equipo de búsqueda del formulario
            cadena_busqueda = request.form.get('cadena', '')
            try:
                # Construir la ruta completa al archivo JSON
                ruta_json = os.path.join(app.root_path, 'static', 'EQUIPOS.json')
                
                # Intentar cargar el archivo JSON
                with open(ruta_json, 'r') as archivo:
                    datos = json.load(archivo)

                # Filtrar los datos según la cadena de búsqueda
                datos_filtrados = [match for match in datos if any(team.startswith(cadena_busqueda) for team in match['teams'])]

                # Si no se encuentran partidos que coincidan, mostrar un mensaje de error
                if not datos_filtrados:
                    mensaje = "No se encontraron resultados para la búsqueda: {}".format(cadena_busqueda)
                    return render_template('lista.html', datos=[], mensaje=mensaje)

                # Almacenar la cadena de búsqueda en la sesión
                session['cadena_busqueda'] = cadena_busqueda

            except FileNotFoundError:
                # Si el archivo no se encuentra, abortar con un error 404
                abort(404)
            
            # Renderizar la plantilla 'lista.html' y pasar los datos filtrados
            return render_template('lista.html', datos=datos_filtrados)
        else:
            # Si la solicitud es GET, redirigir al buscador para evitar enviar un formulario vacío
            return redirect(url_for('buscador'))

@app.route('/detalle/<id_match>')
def detalles(id_match):
        try:
            # Cargar los datos del partido con el ID proporcionado desde el archivo JSON
            with open('static/EQUIPOS.json', 'r') as archivo:
                datos = json.load(archivo)
            
            # Buscar el partido con el ID proporcionado
            partido = next((match for match in datos if match['match_id'] == id_match), None)
            
            if partido:
                # Obtener los detalles del partido
                kickoff_time = partido.get('kickoff_time', '')
                goals = partido.get('goals', {})
                location = partido.get('location', '')

                # Renderizar la plantilla 'detalles.html' y pasar los datos del partido
                return render_template('detalles.html', id_match=id_match, kickoff_time=kickoff_time, goals=goals, location=location)
            else:
                mensaje_error = f"No se encontró ningún partido con el ID {id_match}."

                return mensaje_error, 404
        except FileNotFoundError:
            # Si el archivo no se encuentra, abortar con un error 404
            abort(404)

        return app

if __name__ == "__main__":
    app = crear_app()
    app.run('0.0.0.0', debug=True)

