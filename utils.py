"""
utils.py
Funções auxiliares para o Book Recommender.
"""

import pandas as pd


def filter_by_title(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Filtra o DataFrame por título (busca parcial, case-insensitive)."""
    if not query.strip():
        return df
    mask = df["title"].str.contains(query.strip(), case=False, na=False)
    return df[mask].reset_index(drop=True)


def sort_books(df: pd.DataFrame, sort_by: str, ascending: bool = True) -> pd.DataFrame:
    """
    Ordena o DataFrame.
    sort_by: 'price' | 'rating' | 'title'
    """
    valid = {"price", "rating", "title"}
    if sort_by not in valid or df.empty:
        return df
    return df.sort_values(sort_by, ascending=ascending).reset_index(drop=True)


def paginate(df: pd.DataFrame, page: int, per_page: int = 12) -> tuple[pd.DataFrame, int]:
    """
    Retorna o slice da página solicitada e o total de páginas.
    """
    total = len(df)
    total_pages = max(1, -(-total // per_page))        # divisão inteira arredondada pra cima
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return df.iloc[start:end].reset_index(drop=True), total_pages


def rating_to_stars(rating: int) -> str:
    """Retorna string de estrelas para exibição."""
    return "⭐" * rating + "☆" * (5 - rating)


def build_book_card_html(book: dict) -> str:
    """
    Gera o HTML de um card de livro para exibição no Streamlit via
    st.markdown(..., unsafe_allow_html=True).
    """
    stars = rating_to_stars(book["rating"])
    avail_color = "#27ae60" if "In stock" in book.get("availability", "") else "#e74c3c"

    return f"""
    <div style="
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        background: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
    ">
        <img src="{book['image_url']}"
             style="width:110px; height:155px; object-fit:cover; border-radius:6px;"
             onerror="this.src='https://via.placeholder.com/110x155?text=No+Cover'"/>
        <p style="font-weight:700; font-size:13px; margin:0; line-height:1.3;
                  color:#222; max-height:52px; overflow:hidden;">
            {book['title']}
        </p>
        <p style="font-size:18px; font-weight:800; color:#e67e22; margin:0;">
            {book['price_fmt']}
        </p>
        <p style="font-size:14px; margin:0;" title="{book['rating']} de 5 estrelas">
            {stars}
        </p>
        <p style="font-size:11px; color:{avail_color}; margin:0; font-weight:600;">
            {book.get('availability', '')}
        </p>
        <a href="{book['book_url']}" target="_blank" style="
            display:inline-block; margin-top:4px;
            background:#2980b9; color:white;
            padding:5px 14px; border-radius:20px;
            text-decoration:none; font-size:12px; font-weight:600;
        ">Ver livro →</a>
    </div>
    """