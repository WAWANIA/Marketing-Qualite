import streamlit as st
from product_utils import get_product_info
from image_utils import process_image_and_generate_visual
from io import BytesIO

st.set_page_config(layout="centered")
st.title("Agent Qualité - Générateur d’Illustration Produit")

code_article = st.text_input("Code article")
marque = st.selectbox("Marque", ["ATMOSPHERA", "HESPERIDE", "FIVE"])

if st.button("Générer illustration") and code_article and marque:
    with st.spinner("Traitement en cours..."):
        try:
            produit_image, libelle = get_product_info(code_article, marque)
            if produit_image:
                final_image = process_image_and_generate_visual(produit_image, code_article, libelle)
                st.image(final_image, caption="Illustration qualité générée", use_column_width=True)

                # Convertir l'image en buffer pour téléchargement
                buffer = BytesIO()
                final_image.save(buffer, format="PNG")
                buffer.seek(0)
                st.download_button(
                    label="Télécharger l'image qualité",
                    data=buffer,
                    file_name=f"{code_article}_illustration_qualite.png",
                    mime="image/png"
                )
            else:
                st.error("Produit non trouvé ou structure HTML incompatible.")
        except Exception as e:
            st.error(f"Erreur inattendue : {e}")
