import random
from geopy.distance import great_circle
from itertools import permutations
import folium
from flask import Flask, redirect, render_template, request, url_for
import mysql.connector


app = Flask(__name__)

# Función para conectar con la base de datos y obtener las coordenadas
def obtener_coordenadas():
    # Conecta con la base de datos
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='carlos18',
        database='seguiorden'
    )
    cursor = conn.cursor()

    # Ejecuta una consulta para obtener las coordenadas
    cursor.execute("SELECT IDCoordenada, NombreLugar, Latitud, Longitud FROM Coordenadas")
    coordenadas_db = cursor.fetchall()

    # Convierte las coordenadas a un formato compatible
    locations = [(coordenada[1], float(coordenada[2]), float(coordenada[3])) for coordenada in coordenadas_db]

    # Cierra la conexión con la base de datos
    cursor.close()
    conn.close()

    return locations

# Función para calcular la mejor secuencia de entregas
def calcular_mejor_secuencia(locations):
    # Genera todas las permutaciones posibles de las ubicaciones
    permutaciones_posibles = permutations(range(len(locations)))

    mejor_secuencia = None
    mejor_distancia = float('inf')

    # Encuentra la secuencia de entregas con la distancia total más corta
    for secuencia in permutaciones_posibles:
        distancia_actual = calcular_distancia_total(locations, secuencia)
        if distancia_actual < mejor_distancia:
            mejor_distancia = distancia_actual
            mejor_secuencia = secuencia

    return mejor_secuencia

# Función para calcular la distancia total de una secuencia de entregas

def calcular_distancia_total(locations, secuencia):
    distancia_total = 0
    for i in range(len(secuencia) - 1):
        distancia_total += great_circle(locations[secuencia[i]][1:], locations[secuencia[i + 1]][1:]).meters

    return distancia_total

@app.route('/ruta_optima_map')
def ruta_optima_map():
    locations = obtener_coordenadas()
    mejor_secuencia = calcular_mejor_secuencia(locations)

    # Crea un mapa y agrega marcadores para las ubicaciones
    m = folium.Map(location=locations[mejor_secuencia[0]][1:], zoom_start=8)

    # Agrega una capa de satélite de OpenStreetMap
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='OpenStreetMap',
        name='Mapa',
    ).add_to(m)

    # Agrega una capa de satélite de OpenStreetMap (Esri World Imagery)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery',
        name='Satélite',
    ).add_to(m)

    # Agrega control de capas para cambiar entre la vista de mapa y satélite
    folium.LayerControl().add_to(m)

    # Agrega marcadores y línea de la ruta
    for i, ubicacion in enumerate(mejor_secuencia):
        folium.Marker(
            location=locations[ubicacion][1:],
            popup=locations[ubicacion][0]
        ).add_to(m)

    ruta_optima = [locations[i][1:] for i in mejor_secuencia]
    folium.PolyLine(ruta_optima, color="blue", weight=2.5, opacity=1).add_to(m)

    # Guarda el mapa en un archivo HTML
    m.save("./templates/ruta_optima_map.html")

    return render_template('ruta_optima_map.html', mejor_secuencia=mejor_secuencia)

@app.route('/')
def index():
    locations = obtener_coordenadas()
    mejor_secuencia = calcular_mejor_secuencia(locations)

    return render_template('index.html', ruta_optima=mejor_secuencia, locations=locations)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
