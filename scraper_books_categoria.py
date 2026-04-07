"""
scraper_books_categoria.py
Funções de scraping para books.toscrape.com
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = "https://books.toscrape.com/catalogue/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_page(url: str) -> BeautifulSoup | None:
    """Busca uma página e retorna o objeto BeautifulSoup, ou None em falha."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        print(f"[ERRO] Falha ao buscar {url}: {e}")
        return None


def get_categories() -> dict[str, str]:
    """
    Retorna um dicionário {nome_categoria: url_categoria}
    a partir da sidebar do site.
    """
    soup = fetch_page(BASE_URL)
    if not soup:
        return {}

    categories = {}
    sidebar = soup.find("ul", class_="nav-list")
    if not sidebar:
        return {}

    for li in sidebar.find_all("li"):
        a = li.find("a")
        if a:
            name = a.get_text(strip=True)
            href = a["href"]
            full_url = BASE_URL + href
            if name.lower() != "books":          # ignora o link "All"
                categories[name] = full_url

    return categories


def parse_rating(word: str) -> int:
    """Converte texto de rating ('One', 'Two'…) para inteiro."""
    mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return mapping.get(word, 0)


def scrape_books_from_page(soup: BeautifulSoup, category_url: str) -> list[dict]:
    """Extrai lista de livros de uma única página de categoria."""
    books = []
    articles = soup.find_all("article", class_="product_pod")

    for art in articles:
        # --- Título ---
        title_tag = art.find("h3").find("a")
        title = title_tag["title"]

        # --- Link absoluto ---
        rel_link = title_tag["href"].replace("../", "")
        book_url = CATALOGUE_URL + rel_link

        # --- Imagem ---
        img_tag = art.find("img")
        img_src = img_tag["src"].replace("../", "").replace("../../", "")
        img_url = BASE_URL + img_src

        # --- Preço ---
        price_tag = art.find("p", class_="price_color")
        price_text = price_tag.get_text(strip=True)
        try:
            price = float(price_text.replace("Â", "").replace("£", "").strip())
        except ValueError:
            price = 0.0

        # --- Rating ---
        rating_tag = art.find("p", class_="star-rating")
        rating_word = rating_tag["class"][1] if rating_tag else "Zero"
        rating = parse_rating(rating_word)

        # --- Disponibilidade ---
        avail_tag = art.find("p", class_="availability")
        availability = avail_tag.get_text(strip=True) if avail_tag else "N/A"

        books.append({
            "title": title,
            "price": price,
            "price_fmt": f"£{price:.2f}",
            "rating": rating,
            "rating_stars": "⭐" * rating,
            "image_url": img_url,
            "book_url": book_url,
            "availability": availability,
        })

    return books


def scrape_category(category_url: str, max_pages: int = 5) -> pd.DataFrame:
    """
    Faz scraping de todas as páginas de uma categoria (até max_pages).
    Retorna um DataFrame com todos os livros encontrados.
    """
    all_books = []
    url = category_url

    for page_num in range(1, max_pages + 1):
        soup = fetch_page(url)
        if not soup:
            break

        books = scrape_books_from_page(soup, category_url)
        all_books.extend(books)

        # Verifica se existe próxima página
        next_btn = soup.find("li", class_="next")
        if not next_btn:
            break

        next_href = next_btn.find("a")["href"]
        # Monta URL da próxima página
        base = category_url.rsplit("/", 1)[0] + "/"
        url = base + next_href

    return pd.DataFrame(all_books)