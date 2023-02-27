import os
import shutil
import time
import urllib.parse

import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 3. UTILISER selenium
#    Télécharger les **images seulement** des 2 premières pages du catalogue https://www.zalando.fr/chaussures-homme/.
#    Supprimer les photos non standards (mettant en scène des humains par exemple).

service = Service(executable_path="/home/gcampini/Téléchargements/chromedriver_linux64/chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://www.zalando.fr/chaussures-homme/")

images = driver.find_elements(By.CSS_SELECTOR, "figure img")
urls = [image.get_attribute("src") for image in images]

driver.get("https://www.zalando.fr/chaussures-homme/?p=2")
images = driver.find_elements(By.CSS_SELECTOR, "figure img")
urls += [image.get_attribute("src") for image in images]

# parse urls
urls = [urllib.parse.urlparse(url) for url in urls]

driver.close()

print(f"Found {len(urls)} images")

# Downloading images
path = "images"

if os.path.exists(path):
    shutil.rmtree(path)
os.mkdir(path)

left = len(urls)
for url in urls:
    url = url._replace(query="width=500")
    print(f"Downloading {url.geturl()} ({left} left)")
    filename = os.path.basename(url.path)
    response = requests.get(url.geturl())
    with open(os.path.join(path, filename), "wb") as f:
        f.write(response.content)
    left -= 1

# Supprimer les photos non standards (mettant en scène des humains par exemple)

for filename in os.listdir(path):
    image = Image.open(os.path.join(path, filename))
    top_left = image.getpixel((0, 0))
    top_right = image.getpixel((image.width - 1, 0))
    if top_left != top_right:
        print(f"Removing {filename}")
        os.remove(os.path.join(path, filename))
