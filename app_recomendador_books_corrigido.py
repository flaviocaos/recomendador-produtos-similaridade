
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="📚 Recomendador de Livros - Categorias Reais", layout="wide")

# Mapeamento correto: nome da categoria → slug com ID
CATEGORIAS = {
    "Travel": "travel_2",
    "Mystery": "mystery_3",
    "Historical Fiction": "historical-fiction_4",
    "Sequential Art": "sequential-art_5",
    "Classics": "classics_6",
    "Philosophy": "philosophy_7",
    "Romance": "romance_8",
    "Womens Fiction": "womens-fiction_9",
    "Fiction": "fiction_10",
    "Childrens": "childrens_11",
    "Religion": "religion_12",
    "Nonfiction": "nonfiction_13",
    "Music": "music_14",
    "Science Fiction": "science-fiction_16",
    "Sports and Games": "sports-and-games_17",
    "Fantasy": "fantasy_19",
    "New Adult": "new-adult_20",
    "Young Adult": "young-adult_21",
    "Science": "science_22",
    "Poetry": "poetry_23",
    "Paranormal": "paranormal_24",
    "Art": "art_25",
    "Psychology": "psychology_26",
    "Autobiography": "autobiography_27",
    "Parenting": "parenting_28",
    "Adult Fiction": "adult-fiction_29",
    "Humor": "humor_30",
    "Horror": "horror_31",
    "History": "history_32",
    "Food and Drink": "food-and-drink_33"
}

def buscar_livros_por_categoria(slug):
    url = f"https://books.toscrape.com/catalogue/category/books/{slug}/index.html"
    response = requests.get(url)
    if response.status_code != 200:
        return pd.DataFrame()
    soup = BeautifulSoup(response.text, 'html.parser')
    livros = []

    for article in soup.select("article.product_pod"):
        titulo = article.h3.a["title"]
        preco = article.select_one(".price_color").text.strip()
        imagem = "https://books.toscrape.com/" + article.img["src"].replace("../", "")
        link = "https://books.toscrape.com/catalogue/" + article.h3.a["href"]
        livros.append({
            "titulo": titulo,
            "preco": preco,
            "imagem": imagem,
            "link": link
        })

    return pd.DataFrame(livros)

st.title("📚 Recomendador de Livros por Categoria")

categoria_escolhida = st.selectbox("Selecione uma categoria:", list(CATEGORIAS.keys()))

if categoria_escolhida:
    slug = CATEGORIAS[categoria_escolhida]
    df = buscar_livros_por_categoria(slug)
    if df.empty:
        st.warning("Nenhum livro encontrado para essa categoria.")
    else:
        st.subheader(f"Livros encontrados para: {categoria_escolhida}")
        for _, row in df.iterrows():
            st.markdown(f"### [{row['titulo']}]({row['link']})")
            st.image(row["imagem"], width=120)
            st.markdown(f"**Preço:** {row['preco']}")
            st.markdown("---")
