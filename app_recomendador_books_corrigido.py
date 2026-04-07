"""
app_recomendador_books_corrigido.py
Book Recommender with Real-Time Scraping — v3
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import io

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
    .section-title {
        font-size: 1.3rem; font-weight: 800; color: #1a1a2e;
        margin: 24px 0 12px; border-left: 4px solid #e67e22; padding-left: 12px;
    }
    .pag-info { text-align:center; color:#667eea; font-weight:700; font-size:15px; margin-top:8px; }
    hr { border-color: #e0e8f0 !important; }

    .stButton > button {
        border-radius: 10px !important; font-weight: 700 !important;
        border: none !important;
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
    .stDownloadButton > button {
        border-radius: 10px !important; font-weight: 700 !important;
        border: none !important;
        background: linear-gradient(135deg, #27ae60, #2ecc71) !important;
        color: white !important;
        width: 100%;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 700; font-size: 15px;
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


def df_to_csv(df: pd.DataFrame) -> bytes:
    """Converte DataFrame para CSV em bytes (para download)."""
    cols = ["title", "price_fmt", "rating", "availability", "book_url"]
    return df[cols].rename(columns={
        "title": "Título",
        "price_fmt": "Preço",
        "rating": "Avaliação (1-5)",
        "availability": "Disponibilidade",
        "book_url": "Link",
    }).to_csv(index=False).encode("utf-8")


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
    sort_col = st.selectbox("", ["Relevância", "Preço ↑", "Preço ↓", "Avaliação ↓", "Título A-Z"],
                            label_visibility="collapsed")

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

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS principais
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📖 Livros", "📊 Análises", "🏆 Ranking"])

# ══════════════════════════════════════════════
# TAB 1 — Livros (grade de cards + exportar CSV)
# ══════════════════════════════════════════════
with tab1:
    st.markdown(f'<div class="cat-title">📖 {selected_cat}</div>', unsafe_allow_html=True)

    # Botão exportar CSV
    exp_col1, exp_col2 = st.columns([4, 1])
    with exp_col2:
        csv_bytes = df_to_csv(df_filtered)
        st.download_button(
            label="📥 Exportar CSV",
            data=csv_bytes,
            file_name=f"books_{selected_cat.lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )

    if total_books == 0:
        st.info("🔍 Nenhum livro corresponde à sua busca.")
        st.stop()

    # Paginação
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
            st.markdown(
                f'<div class="pag-info">Página {st.session_state.page} de {total_pages}</div>',
                unsafe_allow_html=True)
        with p3:
            if st.button("Próxima ➡️", disabled=st.session_state.page >= total_pages):
                st.session_state.page += 1
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Grade de cards
    COLS = 4
    rows = [page_df.iloc[i: i + COLS] for i in range(0, len(page_df), COLS)]
    for row in rows:
        cards_html = ""
        for _, book in row.iterrows():
            cards_html += f'<div style="flex:1;min-width:0;padding:8px;">{build_book_card_html(book.to_dict())}</div>'
        empty = COLS - len(row)
        for _ in range(empty):
            cards_html += '<div style="flex:1;min-width:0;padding:8px;"></div>'

        components.html(f"""<!DOCTYPE html><html><head>
        <style>body{{margin:0;padding:0;background:transparent;font-family:sans-serif;}}*{{box-sizing:border-box;}}</style>
        </head><body>
        <div style="display:flex;gap:0;width:100%;">{cards_html}</div>
        </body></html>""", height=420, scrolling=False)


# ══════════════════════════════════════════════
# TAB 2 — Análises (gráficos)
# ══════════════════════════════════════════════
with tab2:
    if df_filtered.empty:
        st.info("Sem dados para exibir.")
    else:
        st.markdown('<div class="section-title">📊 Distribuição de Preços</div>', unsafe_allow_html=True)

        # Histograma de preços via Plotly (embutido como HTML)
        prices = df_filtered["price"].tolist()
        min_p, max_p = min(prices), max(prices)

        # Cria bins manualmente
        import math
        n_bins = min(10, len(set(prices)))
        bin_size = (max_p - min_p) / n_bins if n_bins > 1 else 1
        bins = [min_p + i * bin_size for i in range(n_bins + 1)]
        counts = [0] * n_bins
        for p in prices:
            idx = min(int((p - min_p) / bin_size), n_bins - 1)
            counts[idx] += 1

        bar_labels = [f"£{bins[i]:.0f}–£{bins[i+1]:.0f}" for i in range(n_bins)]
        max_count  = max(counts) if counts else 1
        bar_width  = 540 // n_bins

        bars_svg = ""
        chart_h = 200
        for i, (cnt, lbl) in enumerate(zip(counts, bar_labels)):
            bh = int((cnt / max_count) * chart_h)
            x  = 60 + i * bar_width
            bars_svg += f"""
            <rect x="{x+2}" y="{220 - bh}" width="{bar_width-4}" height="{bh}"
                  fill="url(#grad)" rx="4"/>
            <text x="{x + bar_width//2}" y="{215 - bh}" text-anchor="middle"
                  font-size="11" fill="#667eea" font-weight="700">{cnt}</text>
            <text x="{x + bar_width//2}" y="238" text-anchor="middle"
                  font-size="9" fill="#666" transform="rotate(-30,{x + bar_width//2},238)">{lbl}</text>
            """

        hist_html = f"""
        <svg viewBox="0 0 640 270" xmlns="http://www.w3.org/2000/svg"
             style="width:100%;max-width:700px;display:block;margin:0 auto;">
          <defs>
            <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#667eea"/>
              <stop offset="100%" stop-color="#764ba2"/>
            </linearGradient>
          </defs>
          <text x="320" y="20" text-anchor="middle" font-size="14"
                font-weight="800" fill="#1a1a2e">Distribuição de Preços — {selected_cat}</text>
          <line x1="58" y1="20" x2="58" y2="222" stroke="#ccc" stroke-width="1"/>
          <line x1="58" y1="222" x2="610" y2="222" stroke="#ccc" stroke-width="1"/>
          {bars_svg}
          <text x="10" y="120" text-anchor="middle" font-size="11" fill="#666"
                transform="rotate(-90,10,120)">Qtd. livros</text>
        </svg>
        """
        st.markdown(hist_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">⭐ Distribuição por Avaliação</div>', unsafe_allow_html=True)

        # Gráfico de barras horizontais por rating
        rating_counts = df_filtered["rating"].value_counts().sort_index(ascending=False)
        rating_labels = {5:"★★★★★", 4:"★★★★☆", 3:"★★★☆☆", 2:"★★☆☆☆", 1:"★☆☆☆☆"}
        rating_colors = {5:"#27ae60", 4:"#2ecc71", 3:"#f39c12", 2:"#e67e22", 1:"#e74c3c"}
        max_rc = rating_counts.max() if not rating_counts.empty else 1

        bars_h = ""
        for i, stars in enumerate([5, 4, 3, 2, 1]):
            cnt = rating_counts.get(stars, 0)
            bw  = int((cnt / max_rc) * 400)
            y   = 40 + i * 44
            bars_h += f"""
            <text x="55" y="{y+18}" text-anchor="end" font-size="13"
                  fill="{rating_colors[stars]}" font-weight="700">{rating_labels[stars]}</text>
            <rect x="65" y="{y}" width="{bw}" height="28"
                  fill="{rating_colors[stars]}" rx="6" opacity="0.85"/>
            <text x="{70 + bw}" y="{y+19}" font-size="12"
                  fill="#333" font-weight="700"> {cnt}</text>
            """

        rating_svg = f"""
        <svg viewBox="0 0 520 280" xmlns="http://www.w3.org/2000/svg"
             style="width:100%;max-width:600px;display:block;margin:0 auto;">
          <text x="260" y="22" text-anchor="middle" font-size="14"
                font-weight="800" fill="#1a1a2e">Livros por Avaliação</text>
          {bars_h}
        </svg>
        """
        st.markdown(rating_svg, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 — Ranking Top 10
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🏆 Top 10 Livros Mais Bem Avaliados</div>',
                unsafe_allow_html=True)

    if df_filtered.empty:
        st.info("Sem dados para exibir.")
    else:
        top10 = (df_filtered
                 .sort_values(["rating", "price"], ascending=[False, True])
                 .head(10)
                 .reset_index(drop=True))

        medal = {0: "🥇", 1: "🥈", 2: "🥉"}
        rating_colors = {5:"#27ae60", 4:"#2ecc71", 3:"#f39c12", 2:"#e67e22", 1:"#e74c3c"}

        for i, row in top10.iterrows():
            icon  = medal.get(i, f"#{i+1} ")
            color = rating_colors.get(row["rating"], "#95a5a6")
            stars = "★" * row["rating"] + "☆" * (5 - row["rating"])

            col_rank, col_img, col_info = st.columns([0.5, 1, 6])
            with col_rank:
                st.markdown(
                    f'<div style="font-size:28px;text-align:center;padding-top:20px;">{icon}</div>',
                    unsafe_allow_html=True)
            with col_img:
                st.image(row["image_url"], width=60)
            with col_info:
                st.markdown(f"""
                <div style="padding:10px 0;">
                    <p style="margin:0;font-weight:800;font-size:15px;color:#1a1a2e;">{row['title']}</p>
                    <p style="margin:4px 0 0;">
                        <span style="background:{color};color:white;padding:2px 10px;
                              border-radius:20px;font-size:12px;font-weight:700;">{stars}</span>
                        &nbsp;
                        <span style="font-size:18px;font-weight:800;color:#e67e22;">{row['price_fmt']}</span>
                        &nbsp;
                        <a href="{row['book_url']}" target="_blank"
                           style="font-size:12px;color:#667eea;font-weight:600;">Ver livro →</a>
                    </p>
                </div>
                """, unsafe_allow_html=True)
            st.divider()

        # Exportar Top 10
        st.download_button(
            label="📥 Exportar Top 10 CSV",
            data=df_to_csv(top10),
            file_name=f"top10_{selected_cat.lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )

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