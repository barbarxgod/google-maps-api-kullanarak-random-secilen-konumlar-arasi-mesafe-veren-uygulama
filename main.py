import googlemaps

# API anahtarını kullanarak googlemaps nesnesini oluşturun
gmaps = googlemaps.Client(key="AIzaSyD7m7MFAUoflO1FEdup8wn5fATOVgmHfrQ")

# Balıkesir ilinin sınırlarını çekin
result = gmaps.geocode('Balikesir, Turkey')
print(result)

import random

coordinates = []

# Rastgele 20 nokta seçin
for i in range(20):
    lat = result[0]['geometry']['location']['lat'] + random.uniform(-0.1, 0.1)
    lng = result[0]['geometry']['location']['lng'] + random.uniform(-0.1, 0.1)
    coordinates.append({"lat": lat, "lng": lng})

print(coordinates)

import pandas as pd

# Koordinat bilgilerini DataFrame olarak oluşturun
df = pd.DataFrame(coordinates, columns=["lat", "lng"])

print(df)

from geopy.distance import geodesic

# Mesafe matrisini oluşturun
distance_matrix = []
for i in range(len(coordinates)):
    row = []
    for j in range(len(coordinates)):
        # Her iki nokta arasındaki mesafeyi hesaplayın
        distance = geodesic((coordinates[i]['lat'], coordinates[i]['lng']), (coordinates[j]['lat'], coordinates[j]['lng'])).km
        row.append(distance)
    distance_matrix.append(row)

# Mesafe matrisini gösterin
print(distance_matrix)

from deap import algorithms, base, creator, tools
from deap import tools

# Uygunluk fonksiyonunu tanımlayın
def fitness(individual, distance_matrix):
    total_distance = 0
    for i in range(len(individual)-1):
        total_distance += distance_matrix[individual[i]][individual[i+1]]
    return total_distance,

# Genetik algoritma için gerekli olan nesneleri oluşturun
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

# İlk popülasyonu oluşturun
toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(len(coordinates)), len(coordinates))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("select", tools.selTournament, tournsize=3)

# Uygunluk fonksiyonunu, çaprazlama ve mutasyon operatörlerini tanımlayın
toolbox.register("evaluate", fitness, distance_matrix=distance_matrix)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)

# Genetik algoritmayı çalıştırın
pop = toolbox.population(n=50)
pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.8, mutpb=0.2, ngen=100, verbose=True)


# En iyi individüleri ve uygunluk değerlerini bulun
best_ind = tools.selBest(pop, k=1)[0]
best_distance = fitness(best_ind, distance_matrix)

print("Best Individual: ", best_ind)
print("Best Distance: ", best_distance[0])
for i in range(len(coordinates)):
    for j in range(len(coordinates)):
        print("Nokta {} ile Nokta {} arasındaki mesafe: {:.2f} km".format(i+1, j+1, distance_matrix[i][j]))

import folium

# Harita nesnesini oluşturun
m = folium.Map(location=[result[0]['geometry']['location']['lat'], result[0]['geometry']['location']['lng']], zoom_start=10)




# En kısa rotayı gösteren polyline oluşturun
polyline = folium.PolyLine(locations=[(coordinates[i]['lat'], coordinates[i]['lng']) for i in best_ind], weight=2.5, color='blue')
m.add_child(polyline)

# Noktaları haritada gösterin
for i in range(len(coordinates)):
    folium.Marker(location=[coordinates[i]['lat'], coordinates[i]['lng']],popup=f'Node {i}').add_to(m)

for i in range(len(coordinates)):
    folium.Marker(location=[coordinates[i]['lat'], coordinates[i]['lng']],
                  popup=str(best_ind[i]+1),
                  icon=folium.Icon(color='red')).add_to(m)
# Haritayı gösterin
m.save('map.html')

