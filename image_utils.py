from PIL import Image, ImageDraw, ImageFont
from rembg import remove

def process_image_and_generate_visual(image, code_article, libelle):
    # Détourage
    image = image.convert("RGBA")
    bg_removed = remove(image)

    # Rendu final
    final = bg_removed.copy()
    draw = ImageDraw.Draw(final)

    # Exemple de 3 points + phrases
    points = [(100, 100), (200, 300), (300, 150)]
    phrases = [
        "coins arrondis en plastique renforcé",
        "pédale métal > 20 000 cycles",
        "revêtement anti-UV pour éviter la décoloration"
    ]

    for i, (x, y) in enumerate(points):
        draw.ellipse((x-30, y-30, x+30, y+30), outline="red", width=5)
        draw.text((x+40, y-10), phrases[i], fill="black")

    # Signature
    try:
        avatar = Image.open("assets/avatar_erwan.png").resize((100, 100))
        final.paste(avatar, (20, final.height - 120), avatar)
    except:
        pass  # si avatar manquant

    font = ImageFont.load_default()
    draw.text((130, final.height - 100), "*Erwan, Responsable Qualité vous garantit ce produit*", fill="black", font=font)

    # Code + libellé (en transparence)
    draw.text((20, 20), f"{code_article} - {libelle}", fill=(0, 0, 0, 128), font=font)

    return final
