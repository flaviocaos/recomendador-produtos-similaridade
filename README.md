
# 📚 Book Recommender with Real-Time Scraping

This project is a **web scraper and hybrid product recommender** built with Python, BeautifulSoup, Pandas, and Streamlit. It fetches real-time book data from the public website [books.toscrape.com](https://books.toscrape.com) and displays popular books per category.

---

## 🚀 Features

- ✅ Real-time scraping (no need to download datasets)
- 🔍 Filter by **book category**
- 🖼️ Display title, price, image, and direct link
- 💡 Built as a Streamlit web app
- 💻 Jupyter Notebook version included for experiments

---

## 📂 Project Structure

```
recomendador_books/
├── app_recomendador_books_corrigido.py     # ✅ Final Streamlit app with working categories
├── scraper_books_categoria.ipynb           # 📓 Jupyter notebook with scraping logic
├── README.md                               # 📘 You are here
```

---

## ▶️ Running the App

### 1. Install dependencies

```bash
pip install streamlit pandas beautifulsoup4 requests
```

### 2. Run the app

```bash
streamlit run app_recomendador_books_corrigido.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Jupyter Notebook (Optional)

You can also use the notebook to explore book categories and test scraping logic:

```bash
jupyter notebook scraper_books_categoria.ipynb
```

---

## 📚 Example Categories (English only)

Use category names like:

- `Science Fiction`
- `Fantasy`
- `Mystery`
- `Romance`
- `Travel`
- `Poetry`

---

## ⚠️ Legal Notes

- ✅ This project scrapes from a **public test website**: [books.toscrape.com](https://books.toscrape.com)
- ❌ Do **not** use this logic on commercial sites without respecting `robots.txt` and terms of use.

---

## 📌 License

This project is open-source and provided for educational purposes.

---

## 🤖 Author

Developed by **Flavio Antonio Oliveira da Silva**  
with support from ChatGPT – OpenAI
