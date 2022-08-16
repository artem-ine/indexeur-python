# packages à installer pour que le code fonctionne
from bs4 import BeautifulSoup
from urllib.request import urlopen


def pilote(page, idx, current_depth=0, max_depth=2):
    html_page = urlopen(page)
    soup = BeautifulSoup(html_page, "html.parser")
    links = []
    # limite le nombre de liens qu'on va indexer, modifiable si besoin
    # 3 pour que ça aille plus vite, mais ça marche avec 5, 10, etc :)
    max_links_per_page = 3
    # grâce à beautifulsoup on récupère les liens qui nous intéressent
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        # on dit au code ce qui est une URL absolue/relative
        is_absolute_link = href.startswith('http')
        is_internal_anchor = '#' in href
        # URL absolue :
        if is_absolute_link and not is_internal_anchor:
            links.append(href)
        # URL relative, on pourrait en faire autre chose
        elif not is_internal_anchor:
            # j'ai choisi de les ignorer
            pass
    if current_depth < max_depth:
        # liste créée pour mettre les URLs "à problème"
        # celles-ci peuvent être difficiles à traiter pour différentes raisons
        # afin d'éviter de faire une longue liste d'exception, on les regroupe pour mieux les éviter par la suite
        uglies = []
        for link in links[0:max_links_per_page]:
            try:
                # on utilise la récursivité pour traiter les liens qu'on a déjà trouvés
                pilote(link, index, current_depth=current_depth + 1, max_depth=max_depth)
            # avec try/except on "debug" en live afin d'éviter qu'une erreur empêche l'indexage
            # l'indexe suivra le message indiquant que des URLs ont été ignorés
            # par clarté, on peut éviter de print un message
            # j'ai choisi de le print pour montrer mon cheminement
            except:
                uglies.append(link)
            print(f"J'ai ignoré {len(uglies)} URLs problématiques pour l'indexage choisi.")
            for i, ligne in enumerate(links):
                indexe(idx, ligne.split(), i)


# les fonctions suivantes ont seulement été modifiées pour suivre pilote
# mot est devenu link, etc.
def ajoute(idx, link, ligne):
    if link not in idx:
        idx[link] = []
    if ligne not in idx[link]:
        idx[link].append(ligne)


def indexe(idx, links, ligne):
    for link in links:
        link = link.lower()
        ajoute(idx, link, ligne)


def prd(idx):
    for link in sorted(idx):
        print('\t', link, ':', idx[link])


index = {}
# on teste avec 3 sites différents, les 3 seront indexés ensemble
pilote("https://www.iedparis8.net/?-licence-d-informatique-", index)
pilote("https://docs.python.org/3/", index)
pilote("https://developer.mozilla.org/en-US/", index)
prd(index)
# mycode
