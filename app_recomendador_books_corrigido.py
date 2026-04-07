<<<<<<< HEAD

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
=======
"""
app_recomendador_books_corrigido.py
Book Recommender with Real-Time Scraping
Interface principal em Streamlit.

Execução:
    streamlit run app_recomendador_books_corrigido.py
"""

import streamlit as st
import pandas as pd

from scraper_books_categoria import get_categories, scrape_category
from utils import filter_by_title, sort_books, paginate, build_book_card_html

# ─────────────────────────────────────────────
# Configuração da página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="📚 Book Recommender",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS global
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Header */
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-title {
        font-size: 1rem;
        color: #555;
        text-align: center;
        margin-bottom: 24px;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f0f4f8;
    }
    /* Cards container */
    .stColumn > div { height: 100%; }
    /* Metric personalizado */
    .metric-box {
        background: #2980b9;
        color: white;
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: 700;
        font-size: 15px;
        display: inline-block;
        margin: 4px 4px 16px 0;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Cache: categorias e livros
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_categories() -> dict:
    """Carrega categorias do site (cache de 1 hora)."""
    return get_categories()


@st.cache_data(ttl=1800, show_spinner=False)
def load_books(category_url: str, max_pages: int) -> pd.DataFrame:
    """Faz scraping da categoria e armazena em cache (30 min)."""
    return scrape_category(category_url, max_pages=max_pages)


# ─────────────────────────────────────────────
# Cabeçalho
# ─────────────────────────────────────────────
st.markdown('<h1 class="main-title">📚 Book Recommender</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Scraping em tempo real de '
    '<a href="https://books.toscrape.com" target="_blank">books.toscrape.com</a></p>',
    unsafe_allow_html=True,
)
st.divider()

# ─────────────────────────────────────────────
# Sidebar — filtros
# ─────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://books.toscrape.com/static/oscar/imgs/logo/logo.png",
        use_container_width=True,
    )
    st.markdown("## 🔧 Filtros")

    # Carregar categorias
    with st.spinner("Carregando categorias…"):
        categories = load_categories()

    if not categories:
        st.error("Não foi possível carregar as categorias. Verifique sua conexão.")
        st.stop()

    cat_names = sorted(categories.keys())
    selected_cat = st.selectbox("📂 Categoria", cat_names, index=cat_names.index("Mystery") if "Mystery" in cat_names else 0)

    st.markdown("---")
    st.markdown("### 🔍 Busca por título")
    search_query = st.text_input("Palavras-chave", placeholder="Ex: adventure, love…")

    st.markdown("### ↕️ Ordenação")
    sort_col = st.selectbox("Ordenar por", ["Relevância", "Preço ↑", "Preço ↓", "Avaliação ↓", "Título A-Z"])

    st.markdown("### 📄 Páginas para scraping")
    max_pages = st.slider("Máximo de páginas", min_value=1, max_value=10, value=3,
                          help="Mais páginas = mais livros, porém mais lento na 1ª carga.")

    st.markdown("---")
    clear = st.button("🗑️ Limpar cache e recarregar", use_container_width=True)
    if clear:
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.caption("📌 Dados: [books.toscrape.com](https://books.toscrape.com) · Apenas fins educacionais")

# ─────────────────────────────────────────────
# Scraping principal
# ─────────────────────────────────────────────
cat_url = categories[selected_cat]

with st.spinner(f"🔄 Coletando livros de **{selected_cat}**…"):
    df = load_books(cat_url, max_pages)

if df.empty:
    st.warning(f"Nenhum livro encontrado para a categoria **{selected_cat}**.")
    st.stop()

# ─────────────────────────────────────────────
# Aplicar filtros
# ─────────────────────────────────────────────
df_filtered = filter_by_title(df, search_query)

# Ordenação
sort_map = {
    "Relevância":  (None,     True),
    "Preço ↑":     ("price",  True),
    "Preço ↓":     ("price",  False),
    "Avaliação ↓": ("rating", False),
    "Título A-Z":  ("title",  True),
}
sort_field, asc = sort_map[sort_col]
if sort_field:
    df_filtered = sort_books(df_filtered, sort_field, asc)

# ─────────────────────────────────────────────
# Métricas de resumo
# ─────────────────────────────────────────────
total_books = len(df_filtered)
avg_price   = df_filtered["price"].mean() if total_books else 0
avg_rating  = df_filtered["rating"].mean() if total_books else 0

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("📦 Livros encontrados", total_books)
col_m2.metric("💰 Preço médio",        f"£{avg_price:.2f}")
col_m3.metric("⭐ Avaliação média",    f"{avg_rating:.1f} / 5")

st.markdown(f"### Categoria: {selected_cat}")

if total_books == 0:
    st.info("Nenhum livro corresponde à sua busca.")
    st.stop()

# ─────────────────────────────────────────────
# Paginação
# ─────────────────────────────────────────────
PER_PAGE = 12

# Controle de página no session_state
if "page" not in st.session_state:
    st.session_state.page = 1

# Reset da página ao trocar filtros
filter_key = f"{selected_cat}|{search_query}|{sort_col}"
if st.session_state.get("last_filter") != filter_key:
    st.session_state.page = 1
    st.session_state.last_filter = filter_key

page_df, total_pages = paginate(df_filtered, st.session_state.page, PER_PAGE)

# Navegação
if total_pages > 1:
    pag_cols = st.columns([1, 2, 1])
    with pag_cols[0]:
        if st.button("⬅️ Anterior", disabled=st.session_state.page <= 1):
            st.session_state.page -= 1
            st.rerun()
    with pag_cols[1]:
        st.markdown(
            f"<p style='text-align:center;color:#555;margin-top:6px;'>"
            f"Página <b>{st.session_state.page}</b> de <b>{total_pages}</b></p>",
            unsafe_allow_html=True,
        )
    with pag_cols[2]:
        if st.button("Próxima ➡️", disabled=st.session_state.page >= total_pages):
            st.session_state.page += 1
            st.rerun()

st.markdown("---")

# ─────────────────────────────────────────────
# Grade de cards (4 colunas)
# ─────────────────────────────────────────────
COLS = 4
rows = [page_df.iloc[i : i + COLS] for i in range(0, len(page_df), COLS)]

for row in rows:
    cols = st.columns(COLS)
    for col, (_, book) in zip(cols, row.iterrows()):
        with col:
            st.markdown(build_book_card_html(book.to_dict()), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Rodapé
# ─────────────────────────────────────────────
st.divider()
st.caption(
    "📚 Book Recommender · Dados coletados em tempo real de books.toscrape.com · "
    "Projeto educacional — sem fins comerciais."
)
>>>>>>> 5ae73bbff766625f86da42697f1fe855a8d6977b
