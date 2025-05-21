import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def get_product_info(code_article, marque):
    redirect_urls = {
        "ATMOSPHERA": f"https://www.atmosphera.com/product/search?q={code_article}",
        "HESPERIDE": f"https://www.hesperide.com/product/search?q={code_article}",
        "FIVE": f"https://www.5five.com/product/search?q={code_article}"
    }

    search_url = redirect_urls[marque]
    session = requests.Session()
    response = session.get(search_url, allow_redirects=True)

    if response.status_code != 200:
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')

    image_tag = soup.find("img", {"class": "product-cover"})
    libelle_tag = soup.find("h1")

    if not image_tag or not libelle_tag:
        return None, None

    image_url = image_tag["src"]
    libelle = libelle_tag.text.strip()

    image_data = session.get(image_url).content
    return Image.open(BytesIO(image_data)), libelle
