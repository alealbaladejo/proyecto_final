import requests
import os

def opcion1():
    match_number = input("Por favor, ingresa el número del partido (Por ejemplo 32299): ")
    url = f'https://api.football-data.org/v4/matches/{match_number}/head2head'
    token = os.environ.get('token')
    headers = {'X-Auth-Token': token}
    response = requests.get(url, headers=headers)
    datos = response.json()

    if response.status_code == 404:
        print(f"No se encontró información para el número de partido {match_number}.")
        return
    
    try:
        for match in datos['matches']:
            fecha = match['utcDate']
            jornada = match['matchday']
            competicion = match['competition']['name']
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            home_team_short = match['homeTeam']['shortName']
            away_team_short = match['awayTeam']['shortName']
            home_score = match['score']['fullTime']['home']
            away_score = match['score']['fullTime']['away']
            
            # Verificar si hay árbitros registrados
            if match['referees']:
                arbitro = match['referees'][0]['name']
            else:
                arbitro = "No disponible"
                
            print(f"\n{competicion} | Jornada {jornada} | {fecha}\n{home_team} vs {away_team}")
            print(f"Resultado: {home_team_short} {home_score}-{away_score} {away_team_short}")
            print(f"Árbitro del partido: {arbitro}\n")
    except KeyError:
        print(f"No se encontraron partidos para el número {match_number}.")



def opcion2():
    token = os.environ.get('token')
    headers = {'X-Auth-Token': token}
    url = 'https://api.football-data.org/v4/competitions'
    response = requests.get(url, headers=headers)
    data = response.json()

    # Información de todas las ligas disponibles
    print("Ligas disponibles:")
    for competition in data['competitions']:
        nombre_liga = competition['name']
        iniciales_liga = competition['code']
        print(f"Nombre de la liga: {nombre_liga}, Iniciales de la liga: {iniciales_liga}")

    liga = input("\nPor favor, ingresa las iniciales de la liga que quieres buscar: ")

    # Verificar si la liga existe
    liga_existente = False
    for competition in data['competitions']:
        if competition['code'] == liga:
            liga_existente = True

    if not liga_existente:
        print("Lo siento, la liga ingresada no es válida.")
        return

    temporada = input("Por favor, ingresa el año de la temporada: ")
    url = f'https://api.football-data.org/v4/competitions/{liga}/standings/?season={temporada}'
    response = requests.get(url, headers=headers)
    datos = response.json()

    if response.status_code != 200 or 'standings' not in datos or not datos['standings']:
        print("Lo siento, no se encontraron datos para la temporada proporcionada.")
        return

    for equipo in datos['standings'][0]['table']:
        posicion = equipo['position']
        nombre = equipo['team']['name']
        print(posicion, nombre)

def opcion3():
    url = 'https://api.football-data.org/v4/teams'
    token = os.environ.get('token')
    headers = {'X-Auth-Token': token}
    response = requests.get(url, headers=headers)
    data = response.json()

    print("Equipos disponibles:")
    for equipo in data['teams']:
        print(f" {equipo['id']}, {equipo['name']}")

    codigo = input("\nPor favor, ingresa el ID del equipo a buscar: ")
    url = f'https://api.football-data.org/v4/teams/{codigo}'
    response = requests.get(url, headers=headers)
    datos = response.json()

    # Verificar si se encontraron datos para el equipo
    if response.status_code != 200 or 'message' in datos and datos['message'] == 'The resource you are looking for is restricted':
        print("Lo siento, no se encontraron datos para el ID del equipo proporcionado.")
        return

    # Información general del equipo
    print(f"Nombre: {datos['name']}")
    print(f"Nombre Corto: {datos['shortName']}")
    print(f"TLA: {datos['tla']}")
    print(f"Fundación: {datos['founded']}")
    print(f"Colores del Club: {datos['clubColors']}")
    print(f"Sitio Web: {datos['website']}")
    print(f"Estadio: {datos['venue']}")
    print(f"Dirección: {datos['address']}")

    # Información del entrenador
    if 'coach' in datos:
        mister = datos['coach']
        print("\nEntrenador:")
        print(f"Nombre: {mister['name']}")
        print(f"Fecha de Nacimiento: {mister['dateOfBirth']}")
        print(f"Nacionalidad: {mister['nationality']}")
        print(f"Contrato desde: {mister['contract']['start']}")
        print(f"Contrato hasta: {mister['contract']['until']}")
    else:
        print("\nNo hay información disponible sobre el entrenador.")

    # Información de los jugadores
    if 'squad' in datos:
        print("\nJugadores:")
        for jugador in datos['squad']:
            print(f"Nombre: {jugador['name']}")
            print(f"Posición: {jugador['position']}")
            print(f"Fecha de Nacimiento: {jugador['dateOfBirth']}")
            print(f"Nacionalidad: {jugador['nationality']}\n")
    else:
        print("\nNo hay información disponible sobre los jugadores.")

def menu():
    opcion="a"
    while opcion != "0":
        print('''
            Opción 1. Partidos entre dos equipos.
            Opción 2. Clasificación de una liga.
            Opción 3. Informacin de un equipo.
        ''')
        opcion = input("Introduce una opción del menú: ")
        if opcion == "1":
            opcion1()
        elif opcion == "2":
            opcion2()
        elif opcion == "3":
            opcion3()
        elif opcion == "0":
            print("Saliendo...")
        else:
            print("Eso no es una opción posible. Vuelve a intentarlo (0 para salir)")
menu()