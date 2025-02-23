import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# ======================================
# CONFIGURAÇÃO INICIAL E GERAÇÃO DE DADOS
# ======================================

st.set_page_config(
    page_title="Análise de Vendas",
    layout="wide",
    page_icon="📊"
)

def generate_sales_data():
    np.random.seed(42)
    produtos = [
        {"id_produto": 1, "nome": "Smartphone X", "categoria": "Eletrônicos", "preco": 2500.00},
        {"id_produto": 2, "nome": "Camisa Social", "categoria": "Moda", "preco": 199.90},
        {"id_produto": 3, "nome": "Livro Python Avançado", "categoria": "Livros", "preco": 89.50},
        {"id_produto": 4, "nome": "Mesa de Escritório", "categoria": "Móveis", "preco": 799.00},
        {"id_produto": 5, "nome": "Fone Bluetooth", "categoria": "Eletrônicos", "preco": 150.00}
    ]

    pedidos = []
    start_date = datetime.now() - timedelta(days=540)
    
    for pedido_id in range(1, 51):
        data_pedido = start_date + timedelta(days=np.random.randint(1, 540))
        pedido = {
            "id_pedido": pedido_id,
            "data_pedido": data_pedido,
            "id_cliente": np.random.choice([1, 2, 3]),
            "itens": []
        }
        
        for _ in range(np.random.randint(1, 4)):
            produto = np.random.choice(produtos)
            pedido["itens"].append({
                "id_produto": produto["id_produto"],
                "quantidade": np.random.randint(1, 5),
                "preco_unitario": produto["preco"],
                "categoria": produto["categoria"],
                "nome_produto": produto["nome"]
            })
        
        pedidos.append(pedido)
    
    return pd.DataFrame([(item | {"id_pedido": p["id_pedido"], "data_pedido": p["data_pedido"]})
                      for p in pedidos for item in p["itens"]])

df = generate_sales_data()

# ======================================
# BARRA LATERAL (FILTROS E INFORMAÇÕES)
# ======================================

with st.sidebar:
    st.header("🔍 Filtros de Análise")
    
    categoria = st.selectbox(
        "Selecione a Categoria:",
        options=df['categoria'].unique()
    )
    
    data_min = df['data_pedido'].min().to_pydatetime()
    data_max = df['data_pedido'].max().to_pydatetime()
    data_inicio, data_fim = st.slider(
        "Período de Vendas:",
        min_value=data_min,
        max_value=data_max,
        value=(data_min, data_max),
        format="DD/MM/YYYY"
    )
    
    st.markdown("---")
    st.header("📌 Métricas Chave")
    total_vendas = df['quantidade'].sum()
    st.metric("Total de Unidades Vendidas", f"{total_vendas:,}")
    st.metric("Categorias Disponíveis", len(df['categoria'].unique()))

# ======================================
# CONTEÚDO PRINCIPAL (GRÁFICOS E ANÁLISES)
# ======================================

st.title("Análise Estratégica de Vendas")
df_filtrado = df[
    (df['categoria'] == categoria) &
    (df['data_pedido'].between(data_inicio, data_fim))
]

# Seção 1: Gráficos Principais
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Top 5 Produtos - {categoria}")
    top_produtos = df_filtrado.groupby('nome_produto')['quantidade'].sum().nlargest(5)
    fig1, ax1 = plt.subplots()
    top_produtos.plot(kind='barh', color='#1f77b4', ax=ax1)
    ax1.set_xlabel("Unidades Vendidas")
    st.pyplot(fig1)

with col2:
    st.subheader("Distribuição de Preços")
    fig2, ax2 = plt.subplots()
    ax2.hist(df_filtrado['preco_unitario'], bins=12, edgecolor='black', color='#2ca02c')
    ax2.set_xlabel("Preço Unitário (R$)")
    ax2.set_ylabel("Frequência")
    st.pyplot(fig2)

# Seção 2: Análise Complementar
st.header("Análise Detalhada")
col3, col4 = st.columns(2)
with col3:
    st.subheader("Relação Preço x Quantidade")
    fig3, ax3 = plt.subplots()
    ax3.scatter(df_filtrado['preco_unitario'], df_filtrado['quantidade'], alpha=0.6, color='#d62728')
    ax3.set_xlabel("Preço Unitário (R$)")
    ax3.set_ylabel("Quantidade")
    st.pyplot(fig3)

with col4:
    st.subheader("Distribuição por Categoria")
    fig4, ax4 = plt.subplots()
    df.boxplot(column='preco_unitario', by='categoria', ax=ax4)
    plt.xticks(rotation=45)
    st.pyplot(fig4)

# Seção 3: Tendência Temporal
st.header("Evolução Mensal das Vendas")
fig5, ax5 = plt.subplots(figsize=(10, 4))
df_filtrado.resample('M', on='data_pedido')['quantidade'].sum().plot(
    marker='o',
    linestyle='--',
    color='#9467bd',
    ax=ax5
)
ax5.set_ylabel("Unidades Vendidas")
st.pyplot(fig5)

# Seção 4: Justificativa Técnica
with st.expander("**Justificativa das Análises**"):
    st.write("""
    - **Top Produtos:** Identificação dos produtos mais vendidos para orientar estratégias de reposição.
    - **Distribuição de Preços:** Análise da faixa de preços predominante na categoria selecionada.
    - **Relação Preço x Quantidade:** Verificação de correlação entre preço e volume de vendas (R² = {:.2f}).
    - **Box Plot:** Comparação da distribuição de preços entre categorias para detectar outliers.
    """.format(df_filtrado[['preco_unitario', 'quantidade']].corr().iloc[0,1]))