from geopy.distance import great_circle
from itertools import permutations
import folium
from flask import Flask, render_template

app = Flask(__name__)

# Coordenadas de las ubicaciones
locations = [
    ("Ciudad de México", 19.4326, -99.1332),
    ("Toluca", 19.2925, -99.6569),
    ("Puebla", 19.0402, -98.2062),
    ("Cuernavaca", 18.9242, -99.2216),
    ("Querétaro", 20.5888, -100.3899),
]

# Función para calcular la distancia total de una secuencia de entregas
def calcular_distancia_total(secuencia):
    distancia_total = 0
    for i in range(len(secuencia) - 1):
        distancia_total += great_circle(locations[secuencia[i]][1:], locations[secuencia[i + 1]][1:]).meters
    return distancia_total

# Genera todas las permutaciones posibles de las ubicaciones
permutaciones_posibles = permutations(range(len(locations)))

mejor_secuencia = None
mejor_distancia = float('inf')

# Encuentra la secuencia de entregas con la distancia total más corta
for secuencia in permutaciones_posibles:
    distancia_actual = calcular_distancia_total(secuencia)
    if distancia_actual < mejor_distancia:
        mejor_distancia = distancia_actual
        mejor_secuencia = secuencia

# Crea un mapa y agrega marcadores para las ubicaciones
m = folium.Map(location=locations[mejor_secuencia[0]][1:], zoom_start=8)

for i, ubicacion in enumerate(mejor_secuencia):
    folium.Marker(
        location=locations[ubicacion][1:],
        popup=locations[ubicacion][0],
    ).add_to(m)

# Crea una línea para mostrar la ruta óptima
ruta_optima = [locations[i][1:] for i in mejor_secuencia]
folium.PolyLine(ruta_optima, color="blue", weight=2.5, opacity=1).add_to(m)

# Guarda el mapa en un archivo HTML
m.save("./templates/ruta_optima_map.html")
@app.route('/ruta_optima_map')
def ruta_optima_map():
    return render_template('ruta_optima_map.html', mejor_secuencia=mejor_secuencia)


@app.route('/')
def index():
    return render_template('index.html', ruta_optima=mejor_secuencia, locations=locations)

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port=5000, debug=True)
