import requests
from bs4 import BeautifulSoup
import csv

# Récupérer le contenu de la page web
url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extraire les données des films
movies = []
table = soup.find('table', {'class': 'chart full-width'})
for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    position = cells[1].find('div', {'class': "velocity"}).text.split('\n')[0].strip()
    title = cells[1].find('a').text.strip()
    year = cells[1].find('span', {'class': 'secondaryInfo'}).text.strip('()')
    rating = cells[2].text.strip()
    movie_data = {
        'position': position,
        'title': title,
        'year': year,
        'rating': rating
    }
    movies.append(movie_data)

# Créer un fichier csv representant ces données
with open('movies.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=movies[0].keys())
    writer.writeheader()
    writer.writerows(movies)
