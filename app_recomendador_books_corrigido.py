"""
app_recomendador_books_corrigido.py
Book Recommender with Real-Time Scraping — Visual Melhorado
"""

import streamlit as st
import streamlit.components.v1 as components
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
# CSS Global
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #f5f7fa; }
    .block-container { padding-top: 0 !important; }

    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 0 0 32px 32px;
        padding: 40px 32px 32px;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
    }
    .hero h1 { color: #fff; font-size: 2.8rem; font-weight: 900; margin: 0; }
    .hero p  { color: #a8b8d8; font-size: 1rem; margin: 8px 0 0; }
    .hero a  { color: #667eea; text-decoration: none; font-weight: 600; }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #fff !important; }

    div[data-testid="metric-container"] {
        background: #fff;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
    }
    div[data-testid="metric-container"] label { color: #667eea !important; font-weight: 700; }
    div[data-testid="stMetricValue"] { font-size: 2rem !important; font-weight: 900; color: #1a1a2e !important; }

    .cat-title {
        font-size: 1.6rem; font-weight: 800; color: #1a1a2e;
        margin: 8px 0 16px; border-left: 5px solid #667eea; padding-left: 14px;
    }
    .pag-info { text-align: center; color: #667eea; font-weight: 700; font-size: 15px; margin-top: 8px; }
    hr { border-color: #e0e8f0 !important; }

    .stButton > button {
        border-radius: 10px !important; font-weight: 700 !important;
        border: none !important;
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Cache
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_categories() -> dict:
    return get_categories()


@st.cache_data(ttl=1800, show_spinner=False)
def load_books(category_url: str, max_pages: int) -> pd.DataFrame:
    return scrape_category(category_url, max_pages=max_pages)


# ─────────────────────────────────────────────
# Hero Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>📚 Book Recommender</h1>
    <p>Scraping em tempo real de
    <a href="https://books.toscrape.com" target="_blank">books.toscrape.com</a>
    · Descubra seu próximo livro favorito</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 Book Recommender")
    st.markdown("---")

    with st.spinner("Carregando categorias…"):
        categories = load_categories()

    if not categories:
        st.error("❌ Não foi possível carregar as categorias.")
        st.stop()

    cat_names = sorted(categories.keys())
    default_idx = cat_names.index("Mystery") if "Mystery" in cat_names else 0

    st.markdown("### 📂 Categoria")
    selected_cat = st.selectbox("", cat_names, index=default_idx, label_visibility="collapsed")

    st.markdown("### 🔍 Busca por título")
    search_query = st.text_input("", placeholder="Ex: adventure, dark, love…", label_visibility="collapsed")

    st.markdown("### ↕️ Ordenação")
    sort_col = st.selectbox("", ["Relevância", "Preço ↑", "Preço ↓", "Avaliação ↓", "Título A-Z"], label_visibility="collapsed")

    st.markdown("### 📄 Páginas para scraping")
    max_pages = st.slider("", min_value=1, max_value=10, value=3, label_visibility="collapsed")

    st.markdown("---")
    if st.button("🗑️ Limpar cache e recarregar", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.caption("📌 Apenas fins educacionais · [books.toscrape.com](https://books.toscrape.com)")


# ─────────────────────────────────────────────
# Scraping
# ─────────────────────────────────────────────
cat_url = categories[selected_cat]

with st.spinner(f"🔄 Coletando livros de **{selected_cat}**…"):
    df = load_books(cat_url, max_pages)

if df.empty:
    st.warning(f"⚠️ Nenhum livro encontrado para **{selected_cat}**.")
    st.stop()

# ─────────────────────────────────────────────
# Filtros e ordenação
# ─────────────────────────────────────────────
df_filtered = filter_by_title(df, search_query)

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
# Métricas
# ─────────────────────────────────────────────
total_books = len(df_filtered)
avg_price   = df_filtered["price"].mean() if total_books else 0
avg_rating  = df_filtered["rating"].mean() if total_books else 0
in_stock    = df_filtered["availability"].str.contains("In stock", na=False).sum() if total_books else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Livros encontrados", total_books)
c2.metric("💰 Preço médio",        f"£{avg_price:.2f}")
c3.metric("⭐ Avaliação média",    f"{avg_rating:.1f} / 5")
c4.metric("✅ Em estoque",         in_stock)

st.markdown(f'<div class="cat-title">📖 {selected_cat}</div>', unsafe_allow_html=True)

if total_books == 0:
    st.info("🔍 Nenhum livro corresponde à sua busca.")
    st.stop()

# ─────────────────────────────────────────────
# Paginação
# ─────────────────────────────────────────────
PER_PAGE = 12

if "page" not in st.session_state:
    st.session_state.page = 1

filter_key = f"{selected_cat}|{search_query}|{sort_col}"
if st.session_state.get("last_filter") != filter_key:
    st.session_state.page = 1
    st.session_state.last_filter = filter_key

page_df, total_pages = paginate(df_filtered, st.session_state.page, PER_PAGE)

if total_pages > 1:
    p1, p2, p3 = st.columns([1, 3, 1])
    with p1:
        if st.button("⬅️ Anterior", disabled=st.session_state.page <= 1):
            st.session_state.page -= 1
            st.rerun()
    with p2:
        st.markdown(f'<div class="pag-info">Página {st.session_state.page} de {total_pages}</div>',
                    unsafe_allow_html=True)
    with p3:
        if st.button("Próxima ➡️", disabled=st.session_state.page >= total_pages):
            st.session_state.page += 1
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Grade de cards via components.html (renderiza HTML corretamente)
# ─────────────────────────────────────────────
COLS = 4

rows = [page_df.iloc[i : i + COLS] for i in range(0, len(page_df), COLS)]

for row in rows:
    # Monta uma linha de cards em HTML puro
    cards_html = ""
    for _, book in row.iterrows():
        cards_html += f"""
        <div style="flex:1;min-width:0;padding:8px;">
            {build_book_card_html(book.to_dict())}
        </div>
        """

    # Preenche colunas vazias se a linha tiver menos de COLS livros
    empty = COLS - len(row)
    for _ in range(empty):
        cards_html += '<div style="flex:1;min-width:0;padding:8px;"></div>'

    row_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin:0; padding:0; background:transparent; font-family: sans-serif; }}
        * {{ box-sizing: border-box; }}
    </style>
    </head>
    <body>
        <div style="display:flex;gap:0;width:100%;">
            {cards_html}
        </div>
    </body>
    </html>
    """
    components.html(row_html, height=420, scrolling=False)

# ─────────────────────────────────────────────
# Rodapé
# ─────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;color:#95a5a6;font-size:12px;padding:8px 0;">
    📚 <b>Book Recommender</b> · Dados em tempo real de
    <a href="https://books.toscrape.com" target="_blank" style="color:#667eea;">books.toscrape.com</a>
    · Projeto educacional — sem fins comerciais
</div>
""", unsafe_allow_html=True)