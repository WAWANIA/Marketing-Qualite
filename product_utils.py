import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def get_product_info(code_article, marque):
    base_urls = {
        "ATMOSPHERA": "https://www.atmosphera.com/",
        "HESPERIDE": "https://www.hesperide.com/",
        "FIVE": "https://www.5five.com/"
    }

    url = base_urls[marque] + "recherche?query=" + code_article
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    link = soup.find("a", href=True)
    if not link:
        return None, None

    product_page = requests.get(link['href'])
    product_soup = BeautifulSoup(product_page.text, 'html.parser')

    image_tag = product_soup.find("img", {"class": "product-cover"})
    libelle_tag = product_soup.find("h1")

    if not image_tag or not libelle_tag:
        return None, None

    image_url = image_tag["src"]
    libelle = libelle_tag.text.strip()

    image_data = requests.get(image_url).content
    return Image.open(BytesIO(image_data)), libelle
