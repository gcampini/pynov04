import re

import requests

# 1.      Récuperer le contenu **html** de **l'intégralité** de la page https://fr.wikipedia.org/wiki/Python_(langage).
#         Donner la dernière version de Python à partir du contenu.
#         Combien de liens menant vers Wikipédia au sein de la page ?

html = requests.get("https://fr.wikipedia.org/wiki/Python_(langage)").text

# without regex
index = html.find("Dernière version")
text_after = html[index:]

start = text_after.find("\">") + 2
end = text_after.find("(") - 1

version = text_after[start:end]
print(version)

# with regex
match = re.search(
    r"Dernière version.*?(\d+\.\d+\.\d+)",
    html,
    re.S)
version = match.group(1)
print(version)

links = re.findall(r"href=\"\/wiki\/", html)
print(f"Number of links: {len(links)}")
