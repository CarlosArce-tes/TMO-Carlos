import random
from geopy.distance import great_circle
from itertools import permutations
import folium
from flask import Flask, jsonify,render_template, redirect, url_for
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
def obtener_coordenadas():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='carlos18',
        database='seguiorden'
    )
    cursor = conn.cursor()

    cursor.execute("SELECT IDCoordenada, NombreLugar, Latitud, Longitud, Status FROM Coordenadas WHERE Status=0 ")
    coordenadas_db = cursor.fetchall()

    # Correct the variable name to 'coordenada' in the list comprehension
    locations = [(coordenada[0], coordenada[1], float(coordenada[2]), float(coordenada[3])) for coordenada in coordenadas_db]

    cursor.close()
    conn.close()

    return locations
def obtenerEntregados():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='carlos18',
        database='seguiorden'
    )
    cursor = conn.cursor()

    cursor.execute("SELECT IDCoordenada, NombreLugar, Latitud, Longitud, Status FROM Coordenadas WHERE Status=1 ")
    coordenadas_db = cursor.fetchall()

    # Correct the variable name to 'coordenada' in the list comprehension
    locations2 = [(coordenada[0], coordenada[1], float(coordenada[2]), float(coordenada[3])) for coordenada in coordenadas_db]

    cursor.close()
    conn.close()
    return locations2


def calcular_mejor_secuencia(locations):
    permutaciones_posibles = permutations(range(len(locations)))
    mejor_secuencia = None
    mejor_distancia = float('inf')

    for secuencia in permutaciones_posibles:
        distancia_actual = calcular_distancia_total(locations, secuencia)
        if distancia_actual < mejor_distancia:
            mejor_distancia = distancia_actual
            mejor_secuencia = secuencia

    return mejor_secuencia

def calcular_distancia_total(locations, secuencia):
    distancia_total = 0
    for i in range(len(secuencia) - 1):
        distancia_total += great_circle(locations[secuencia[i]][2:], locations[secuencia[i + 1]][2:]).meters

    return distancia_total

@app.route('/ruta_optima_map')
def ruta_optima_map():
    locations = obtener_coordenadas()
    mejor_secuencia = calcular_mejor_secuencia(locations)
    
    m = folium.Map(location=locations[mejor_secuencia[0]][2:], zoom_start=8)

    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='OpenStreetMap',
        name='Mapa',
    ).add_to(m)

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery',
        name='Satélite',
    ).add_to(m)


    folium.LayerControl().add_to(m)

    for i, ubicacion in enumerate(mejor_secuencia):
        folium.Marker(
            location=locations[ubicacion][2:],
            popup=f'{locations[ubicacion][0]} \n {locations[ubicacion][1]} \n {locations[ubicacion][2]} \n {locations[ubicacion][3]}'
        ).add_to(m)

    ruta_optima = [locations[i][2:] for i in mejor_secuencia]
    folium.PolyLine(ruta_optima, color="blue", weight=2.5, opacity=1).add_to(m)

    m.save("./templates/ruta_optima_map.html")
    



    return render_template('ruta_optima_map.html', mejor_secuencia=mejor_secuencia)

    
@app.route('/')
def index():
    nombre = 'carlos'
    locations = obtener_coordenadas()
    mejor_secuencia = calcular_mejor_secuencia(locations)
    locations2 = obtenerEntregados()
    totalEntrega = contadorEntregas()
    noentregado = contadorNoEntregas()
    return render_template('index.html', ruta_optima=mejor_secuencia, locations=locations, nombre=nombre, locations2= locations2, totalEntrega=totalEntrega, noentregado=noentregado)

@app.route('/eliminar_ubicacion/<int:id>')
def eliminar_ubicacion(id):
    print(f"Received ID: {id}")

    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='carlos18',
        database='seguiorden'
    )
    cursor = conn.cursor()

    cursor.execute("UPDATE Coordenadas SET Status=1 WHERE IDCoordenada = %s", (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('index'))
def contadorEntregas():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='carlos18',
        database='seguiorden'
    )
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS entregas FROM Coordenadas WHERE Status = 1")

    # Recuperar el resultado
    resultado = cursor.fetchone()
    total_entregas = resultado[0] if resultado else None

    # Cerrar cursor y conexión
    cursor.close()
    conn.close()

    return total_entregas

def contadorNoEntregas():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='carlos18',
        database='seguiorden'
    )
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS entregas FROM Coordenadas WHERE Status = 0")

    # Recuperar el resultado
    resultado2 = cursor.fetchone()
    totalnoentregas = resultado2[0] if resultado2 else None

    # Cerrar cursor y conexión
    cursor.close()
    conn.close()

    return totalnoentregas

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

#insert seguimieto orden