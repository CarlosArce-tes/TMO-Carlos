import folium
import osmnx as ox
from itertools import permutations

# Coordenadas de las ubicaciones
locations = [
    ("Reforma 222, Ciudad de México", 19.4276, -99.1675),
    ("Ángel de la Independencia, Ciudad de México", 19.4270, -99.1676),
    ("Zona Rosa, Ciudad de México", 19.4257, -99.1655),
    ("Condesa, Ciudad de México", 19.4144, -99.1768),
    ("Roma, Ciudad de México", 19.4150, -99.1574),
]

# Función para calcular la distancia total de una secuencia de entregas
def calcular_distancia_total(secuencia):
    distancia_total = 0
    for i in range(len(secuencia) - 1):
        origen = locations[secuencia[i]][1], locations[secuencia[i]][2]
        destino = locations[secuencia[i + 1]][1], locations[secuencia[i + 1]][2]
        
        # Descarga datos de OpenStreetMap para el área del viaje
        grafo = ox.graph_from_point(origen, dist=20000, network_type='all')

        # Calcula la distancia de la ruta
        ruta = ox.shortest_path(grafo, origen, destino, weight='length')
        distancia = sum(ox.utils_graph.get_route_edge_attributes(grafo, ruta, 'length'))

        distancia_total += distancia
    
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

# Imprime la secuencia óptima de entregas y la distancia total óptima
print("Ubicaciones:")
for i, ubicacion in enumerate(mejor_secuencia):
    print(f"{i + 1}. {locations[ubicacion][0]}")

print(f"Distancia total óptima por carretera: {mejor_distancia} metros")

# Crea un mapa y agrega marcadores para las ubicaciones
m = folium.Map(location=locations[mejor_secuencia[0]][1:], zoom_start=5)

for i, ubicacion in enumerate(mejor_secuencia):
    folium.Marker(
        location=locations[ubicacion][1:],
        popup=locations[ubicacion][0],
    ).add_to(m)

# Crea una línea para mostrar la ruta óptima
ruta_optima = [locations[i][1:] for i in mejor_secuencia]
folium.PolyLine(ruta_optima, color="blue", weight=2.5, opacity=1).add_to(m)

# Guarda el mapa en un archivo HTML
m.save("ruta_optima.html")
