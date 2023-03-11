# 4. Récupérer les informations météo actuelles (https://open-meteo.com/) à Aix.
#    Donner les minimales et maximales de températures et quand elles interviennent.

import requests
import json

# Récupération des données
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 43.529742,
    "longitude": 5.447427,
    "hourly": "temperature_2m",
    "timezone": "Europe/Paris",
}
response = requests.get(url, params=params)
data = json.loads(response.text)

# Affichage des données
min_index = None
max_index = None

for i, temp in enumerate(data["hourly"]["temperature_2m"]):
    if min_index is None or temp < data["hourly"]["temperature_2m"][min_index]:
        min_index = i
    if max_index is None or temp > data["hourly"]["temperature_2m"][max_index]:
        max_index = i

min_date = data["hourly"]["time"][min_index].split("T")[1]
min_temp = data["hourly"]["temperature_2m"][min_index]

max_date = data["hourly"]["time"][max_index].split("T")[1]
max_temp = data["hourly"]["temperature_2m"][max_index]

print(f"Min: {min_temp}°C à {min_date}")
print(f"Max: {max_temp}°C à {max_date}")