<<<<<<< HEAD

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
=======
# 📚 Book Recommender with Real-Time Scraping

Aplicativo web em **Streamlit** que recomenda livros por categoria, coletando dados
em tempo real do site público [books.toscrape.com](https://books.toscrape.com).

---

## 🗂️ Estrutura do Projeto

```
book-recommender/
├── app_recomendador_books_corrigido.py  # App principal (Streamlit)
├── scraper_books_categoria.py           # Funções de scraping
├── utils.py                             # Funções auxiliares
└── README.md
>>>>>>> 5ae73bbff766625f86da42697f1fe855a8d6977b
```

---

<<<<<<< HEAD
## ▶️ Running the App

### 1. Install dependencies
=======
## 🚀 Instalação e Execução

### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/seu-usuario/book-recommender.git
cd book-recommender
```

### 2. (Recomendado) Crie um ambiente virtual

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Instale as dependências
>>>>>>> 5ae73bbff766625f86da42697f1fe855a8d6977b

```bash
pip install streamlit pandas beautifulsoup4 requests
```

<<<<<<< HEAD
### 2. Run the app
=======
### 4. Execute o app
>>>>>>> 5ae73bbff766625f86da42697f1fe855a8d6977b

```bash
streamlit run app_recomendador_books_corrigido.py
```

<<<<<<< HEAD
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
=======
O app abrirá automaticamente no navegador em `http://localhost:8501`.

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| 📂 Seleção de categoria | Sidebar com todas as categorias do site |
| 🔍 Busca por título | Filtro por palavras-chave |
| ↕️ Ordenação | Por preço (↑↓), avaliação ou título |
| 🃏 Cards visuais | Grade de 4 colunas com capa, preço, rating e link |
| 📄 Paginação | 12 livros por página |
| ⚡ Cache inteligente | Categorias cacheadas por 1h, livros por 30min |
| 🗑️ Limpar cache | Botão para forçar re-scraping |
| 📊 Métricas | Total de livros, preço médio, avaliação média |

---

## 🗃️ Categorias suportadas (exemplos)

- Science Fiction
- Fantasy
- Mystery
- Romance
- Travel
- Poetry
- History
- Horror
- Classics
- … e todas as demais disponíveis no site

---

## 🔧 Configurações

No slider da sidebar, escolha quantas **páginas** do site serão coletadas
(1–10). Cada página contém ~20 livros. O cache evita scraping redundante.

---

## 🏗️ Expansão futura

- [ ] Recomendação por similaridade (TF-IDF ou embeddings)
- [ ] Ranking de popularidade composto (preço + rating)
- [ ] Download dos dados como CSV
- [ ] Detalhes individuais de cada livro (descrição, UPC)
- [ ] Deploy no Streamlit Cloud

---

## ⚖️ Observações

- O site `books.toscrape.com` é **público e criado para fins educacionais**.
- Nenhum dado sensível é coletado ou armazenado.
- Não use este scraper em sites sem permissão explícita.

---

## 📦 Dependências

```
streamlit>=1.30
pandas>=2.0
beautifulsoup4>=4.12
requests>=2.31
```
>>>>>>> 5ae73bbff766625f86da42697f1fe855a8d6977b
