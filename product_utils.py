import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def get_product_info(code_article, marque):
    base_urls = {
        "ATMOSPHERA": "https://www.atmosphera.com/recherche?query=",
        "HESPERIDE": "https://www.hesperide.com/recherche?query=",
        "FIVE": "https://www.5five.com/recherche?query="
    }

    if marque not in base_urls:
        return None, None

    search_url = base_urls[marque] + code_article
    headers = {"User-Agent": "Mozilla/5.0"}
    session = requests.Session()
    response = session.get(search_url, headers=headers)

    if response.status_code != 200:
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    product_link_tag = soup.find("a", href=True)
    if not product_link_tag:
        return None, None

    product_url = product_link_tag["href"]
    if not product_url.startswith("http"):
        domain = base_urls[marque].split("/recherche")[0]
        product_url = domain + product_url

    product_page = session.get(product_url, headers=headers)
    if product_page.status_code != 200:
        return None, None

    product_soup = BeautifulSoup(product_page.text, 'html.parser')
    image_tag = product_soup.find("img", {"class": "product-cover"})
    libelle_tag = product_soup.find("h1")

    if not image_tag or not libelle_tag:
        return None, None

    image_url = image_tag["src"]
    libelle = libelle_tag.text.strip()
    image_data = session.get(image_url, headers=headers).content

    image = Image.open(BytesIO(image_data))
    image.verify()  # Vérifie que l’image est lisible
    image = Image.open(BytesIO(image_data))  # Recharger pour usage

    return image, libelle
