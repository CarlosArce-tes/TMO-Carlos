from geopy.distance import great_circle
from itertools import permutations

# Coordenadas de los puntos de entrega y recolección
locations = [
    (40.7128, -74.0060),  # Nueva York, NY
    (34.0522, -118.2437),  # Los Ángeles, CA
    (41.8781, -87.6298),  # Chicago, IL
    (37.7749, -122.4194),  # San Francisco, CA
]

# Función para calcular la distancia total de una secuencia de entregas
def calcular_distancia_total(secuencia):
    distancia_total = 0
    for i in range(len(secuencia) - 1):
        distancia_total += great_circle(locations[secuencia[i]], locations[secuencia[i + 1]]).meters
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

print(f"Secuencia óptima de entregas: {mejor_secuencia}")
print(f"Distancia total óptima: {mejor_distancia} metros")
