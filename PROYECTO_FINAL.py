import requests
from config import TOKEN

def opcion1():
    url = 'https://api.football-data.org/v4/matches/32299/head2head'
    headers = {'X-Auth-Token': TOKEN}
    response = requests.get(url, headers=headers)
    datos = response.json()
    
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
        arbitro = match['referees'][0]['name']
            
        print(f"{competicion} | Jornada {jornada} | {fecha}\n{home_team} vs {away_team}")
        print(f"Resultado: {home_team_short} {home_score}-{away_score} {away_team_short}")
        print(f"Árbitro del partido: {arbitro}\n")


def opcion2():
    url = 'https://api.football-data.org/v4/competitions/PD/standings/?season=2022'
    headers = {'X-Auth-Token': TOKEN}
    response = requests.get(url, headers=headers)
    datos = response.json()

    for equipo in datos['standings'][0]['table']:
        posicion = equipo['position']
        nombre = equipo ['team']['name']
        print(posicion, nombre)
        
def opcion3():
    url = 'https://api.football-data.org/v4/teams/90'
    headers = {'X-Auth-Token': TOKEN}
    response = requests.get(url, headers=headers)
    datos = response.json()

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
    mister = datos['coach']
    print("\nEntrenador:")
    print(f"Nombre: {mister['name']}")
    print(f"Fecha de Nacimiento: {mister['dateOfBirth']}")
    print(f"Nacionalidad: {mister['nationality']}")
    print(f"Contrato desde: {mister['contract']['start']}")
    print(f"Contrato hasta: {mister['contract']['until']}")

    # Información de los jugadores
    print("\nJugadores:")
    for jugador in datos['squad']:
        print(f"Nombre: {jugador['name']}")
        print(f"Posición: {jugador['position']}")
        print(f"Fecha de Nacimiento: {jugador['dateOfBirth']}")
        print(f"Nacionalidad: {jugador['nationality']}\n")


def menu():
    opcion="a"
    while opcion != "0":
        print('''
            Opción 1. Partidos entre Chelsea y Manchester United
            Opción 2. Clasificación de la Liga Española del año 2022.
            Opción 3. Información del Real Betis.
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