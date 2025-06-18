
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Dados simulados
produtos = pd.DataFrame({
    'produto_id': range(1, 11),
    'nome': [
        'Notebook Gamer', 'Smartphone 5G', 'Tênis Esportivo', 'Relógio Digital',
        'Fone Bluetooth', 'Câmera Fotográfica', 'Smart TV 50\"', 'Tablet 10\"',
        'Mouse Ergonômico', 'Teclado Mecânico'
    ],
    'descricao': [
        'Notebook com placa de vídeo dedicada e SSD rápido',
        'Smartphone com tecnologia 5G, ótima câmera e bateria duradoura',
        'Tênis leve e confortável para corrida ou academia',
        'Relógio com cronômetro, bluetooth e bateria longa',
        'Fone sem fio com cancelamento de ruído e microfone',
        'Câmera com lente intercambiável e zoom óptico poderoso',
        'Smart TV com resolução 4K, HDR e sistema Android',
        'Tablet com boa autonomia, ideal para leitura e vídeos',
        'Mouse ergonômico com vários botões programáveis',
        'Teclado mecânico com iluminação RGB e switches azuis'
    ]
})

# Vetorização TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(produtos['descricao'])
similaridade = cosine_similarity(tfidf_matrix)

# Função de recomendação
def recomendar_produtos(produto_id, top_n=3):
    idx = produtos[produtos['produto_id'] == produto_id].index[0]
    scores = list(enumerate(similaridade[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recomendacoes = produtos.iloc[[i[0] for i in scores]]
    return recomendacoes[['produto_id', 'nome']]

# Streamlit app
st.title("🔍 Recomendador de Produtos por Similaridade")
escolhido = st.selectbox("Selecione um produto:", produtos['nome'].tolist())

if escolhido:
    produto_id = produtos[produtos['nome'] == escolhido]['produto_id'].values[0]
    st.subheader("Recomendações:")
    resultados = recomendar_produtos(produto_id)
    st.dataframe(resultados.reset_index(drop=True))
