"""
utils.py
Funções auxiliares para o Book Recommender.
"""

import pandas as pd


def filter_by_title(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query.strip():
        return df
    mask = df["title"].str.contains(query.strip(), case=False, na=False)
    return df[mask].reset_index(drop=True)


def sort_books(df: pd.DataFrame, sort_by: str, ascending: bool = True) -> pd.DataFrame:
    valid = {"price", "rating", "title"}
    if sort_by not in valid or df.empty:
        return df
    return df.sort_values(sort_by, ascending=ascending).reset_index(drop=True)


def paginate(df: pd.DataFrame, page: int, per_page: int = 12) -> tuple[pd.DataFrame, int]:
    total = len(df)
    total_pages = max(1, -(-total // per_page))
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return df.iloc[start:end].reset_index(drop=True), total_pages


def rating_badge(rating: int) -> str:
    """Retorna badge colorido baseado no rating."""
    colors = {5: "#27ae60", 4: "#2ecc71", 3: "#f39c12", 2: "#e67e22", 1: "#e74c3c"}
    color = colors.get(rating, "#95a5a6")
    stars = "★" * rating + "☆" * (5 - rating)
    return f'<span style="background:{color};color:white;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:700;">{stars}</span>'


def build_book_card_html(book: dict) -> str:
    """Gera HTML de card moderno com hover effect."""
    avail_color = "#27ae60" if "In stock" in book.get("availability", "") else "#e74c3c"
    avail_icon = "✅" if "In stock" in book.get("availability", "") else "❌"
    badge = rating_badge(book["rating"])

    return f"""
    <div style="
        border: none;
        border-radius: 16px;
        padding: 0;
        background: #ffffff;
        box-shadow: 0 4px 20px rgba(0,0,0,0.10);
        overflow: hidden;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
        display: flex;
        flex-direction: column;
    " onmouseover="this.style.transform='translateY(-6px)';this.style.boxShadow='0 12px 32px rgba(0,0,0,0.18)'"
       onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 20px rgba(0,0,0,0.10)'">

        <!-- Imagem -->
        <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);padding:20px;text-align:center;">
            <img src="{book['image_url']}"
                 style="width:110px;height:155px;object-fit:cover;border-radius:8px;
                        box-shadow:0 8px 24px rgba(0,0,0,0.4);"
                 onerror="this.src='https://via.placeholder.com/110x155?text=No+Cover'"/>
        </div>

        <!-- Conteúdo -->
        <div style="padding:16px;display:flex;flex-direction:column;gap:8px;flex:1;">
            <p style="font-weight:700;font-size:13px;margin:0;line-height:1.4;
                      color:#1a1a2e;min-height:36px;overflow:hidden;
                      display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;">
                {book['title']}
            </p>

            <div style="display:flex;align-items:center;justify-content:space-between;">
                <p style="font-size:22px;font-weight:800;color:#e67e22;margin:0;">
                    {book['price_fmt']}
                </p>
                {badge}
            </div>

            <p style="font-size:11px;color:{avail_color};margin:0;font-weight:600;">
                {avail_icon} {book.get('availability', '')}
            </p>

            <a href="{book['book_url']}" target="_blank" style="
                display:block;margin-top:auto;padding-top:8px;
                background:linear-gradient(135deg,#667eea,#764ba2);
                color:white;padding:9px 0;border-radius:10px;
                text-decoration:none;font-size:13px;font-weight:700;
                text-align:center;letter-spacing:0.5px;
            ">🔗 Ver livro</a>
        </div>
    </div>
    """