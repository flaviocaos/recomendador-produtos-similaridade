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
```

---

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

```bash
pip install streamlit pandas beautifulsoup4 requests
```

### 4. Execute o app

```bash
streamlit run app_recomendador_books_corrigido.py
```

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
