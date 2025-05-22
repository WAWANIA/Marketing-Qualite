import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def get_product_info(code_article, marque):
    debug_log = []
    base_urls = {
        "ATMOSPHERA": "https://www.atmosphera.com/recherche?query=",
        "HESPERIDE": "https://www.hesperide.com/recherche?query=",
        "FIVE": "https://www.5five.com/recherche?query="
    }

    if marque not in base_urls:
        debug_log.append("Marque non reconnue.")
        return None, None, debug_log

    search_url = base_urls[marque] + code_article
    debug_log.append(f"URL de recherche : {search_url}")
    headers = {"User-Agent": "Mozilla/5.0"}
    session = requests.Session()
    response = session.get(search_url, headers=headers)

    if response.status_code != 200:
        debug_log.append(f"Échec de la requête de recherche : {response.status_code}")
        return None, None, debug_log

    soup = BeautifulSoup(response.text, 'html.parser')
    candidate_links = [
        a["href"] for a in soup.find_all("a", href=True)
        if not a["href"].startswith("javascript") and not a["href"].startswith("#")
    ]

    product_url = None
    for link in candidate_links:
        full_url = link if link.startswith("http") else base_urls[marque].split("/recherche")[0] + link
        product_page = session.get(full_url, headers=headers)
        page_soup = BeautifulSoup(product_page.text, 'html.parser')
        image_tag = page_soup.find("img", {"class": "product-cover"})
        libelle_tag = page_soup.find("h1")
        if image_tag and libelle_tag:
            product_url = full_url
            break

    if not product_url:
        debug_log.append("Aucune fiche produit valide trouvée (image + libellé manquants).")
        return None, None, debug_log

    debug_log.append(f"Lien fiche produit retenu : {product_url}")
    product_soup = BeautifulSoup(product_page.text, 'html.parser')
    image_tag = product_soup.find("img", {"class": "product-cover"})
    libelle_tag = product_soup.find("h1")

    image_url = image_tag["src"]
    if not image_url.startswith("http"):
        domain = base_urls[marque].split("/recherche")[0]
        image_url = domain + image_url
    debug_log.append(f"Image URL : {image_url}")

    try:
        image_data = session.get(image_url, headers=headers).content
        image = Image.open(BytesIO(image_data))
        image.verify()
        image = Image.open(BytesIO(image_data))
        debug_log.append("Image chargée et vérifiée avec succès.")
    except Exception as e:
        debug_log.append(f"Erreur lors du chargement de l'image : {e}")
        return None, None, debug_log

    libelle = libelle_tag.text.strip()
    return image, libelle, debug_log
