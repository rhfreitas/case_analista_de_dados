import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import io

# Configuração da página
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# ========== Funções para Gerar Dados ==========
def gerar_dados_vendas():
    datas = pd.date_range(end=datetime.now(), periods=12, freq='M')
    return pd.DataFrame({
        'mes_ano': [d.strftime('%Y-%m') for d in datas],
        'total_vendas': np.random.uniform(80000, 120000, 12).round(2),
        'custo': np.random.uniform(40000, 60000, 12).round(2)
    }).assign(
        lucro = lambda df: df['total_vendas'] - df['custo'],
        crescimento = lambda df: (df['total_vendas'].pct_change() * 100).round(2)
    )

def gerar_dados_rfm():
    return pd.DataFrame({
        'id_cliente': range(1, 101),
        'ultima_compra': [datetime.now() - timedelta(days=np.random.randint(1, 365)) for _ in range(100)],
        'frequencia': np.random.randint(1, 50, 100),
        'valor_total': np.random.uniform(1000, 10000, 100).round(2)
    }).assign(
        segmento = lambda df: pd.qcut(df['valor_total'], 3, labels=['Bronze', 'Prata', 'Ouro'])
    )

def gerar_dados_produtos():
    return pd.DataFrame({
        'produto_id': range(1, 21),
        'nome': [f'Produto {i}' for i in range(1, 21)],
        'categoria': np.random.choice(['Eletrônicos', 'Vestuário', 'Alimentos'], 20),
        'preco': np.random.uniform(50, 1000, 20).round(2),
        'vendas': np.random.randint(100, 1000, 20)
    }).assign(
        receita = lambda df: df['preco'] * df['vendas']
    )

def gerar_dados_clientes_inativos():
    return pd.DataFrame({
        'id_cliente': range(1, 51),
        'ultima_compra': [datetime.now() - timedelta(days=np.random.randint(180, 365)) for _ in range(50)],
        'valor_total': np.random.uniform(500, 5000, 50).round(2)
    })

# ========== Componentes do Dashboard ==========
def filtros_sidebar():
    st.sidebar.title("Filtros Avançados")
    return {
        'data_inicio': st.sidebar.date_input("Data inicial", datetime.now() - timedelta(days=365)),
        'data_fim': st.sidebar.date_input("Data final", datetime.now()),
        'segmento': st.sidebar.multiselect("Segmentos", ['Bronze', 'Prata', 'Ouro'], default=['Ouro'])
    }

def exportar_dados(df, nome):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:  # Corrigido
        df.to_excel(writer, index=False)
    st.download_button(
        f"📥 Exportar {nome} (Excel)",
        data=buffer.getvalue(),
        file_name=f"{nome}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ========== Visualizações ==========
def visao_geral():
    st.header("Visão Estratégica")
    dados = gerar_dados_vendas()
    
    # KPIs
    cols = st.columns(4)
    cols[0].metric("Receita Total", f"R$ {dados['total_vendas'].sum():,.2f}")
    cols[1].metric("Lucro Total", f"R$ {dados['lucro'].sum():,.2f}")
    cols[2].metric("Custo Total", f"R$ {dados['custo'].sum():,.2f}")
    cols[3].metric("Crescimento Médio", f"{dados['crescimento'].mean():.1f}%")
    
    # Gráficos
    fig = px.line(dados, x='mes_ano', y=['total_vendas', 'custo'], title='Desempenho Financeiro')
    st.plotly_chart(fig, use_container_width=True)
    exportar_dados(dados, 'desempenho_financeiro')

def analise_rfm(filtros):
    st.header("Segmentação RFM")
    dados = gerar_dados_rfm().query("segmento in @filtros['segmento']")
    
    # Gráficos
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.box(dados, x='segmento', y='valor_total', title='Distribuição por Segmento')
        st.plotly_chart(fig1)
        
    with col2:
        fig2 = px.scatter(dados, x='frequencia', y='valor_total', color='segmento', 
                        hover_data=['ultima_compra'], title='Frequência vs Valor')
        st.plotly_chart(fig2)
    
    exportar_dados(dados, 'rfm')

def top_produtos():
    st.header("Top Produtos")
    dados = gerar_dados_produtos().nlargest(5, 'receita')
    
    fig = px.bar(dados, x='nome', y='receita', color='categoria', 
                title='Top 5 Produtos por Receita')
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(
        dados.style.format({
            'preco': 'R$ {:.2f}',
            'receita': 'R$ {:.2f}'
        }), 
        hide_index=True
    )
    exportar_dados(dados, 'top_produtos')

def tendencias_vendas():
    st.header("Tendências de Vendas")
    dados = gerar_dados_vendas()
    
    fig = px.area(dados, x='mes_ano', y='total_vendas', title='Vendas Mensais')
    st.plotly_chart(fig, use_container_width=True)
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=dados['mes_ano'], y=dados['crescimento'], 
                            mode='lines+markers', name='Crescimento'))
    fig2.update_layout(title='Taxa de Crescimento Mensal')
    st.plotly_chart(fig2, use_container_width=True)
    exportar_dados(dados, 'tendencias_vendas')

def clientes_inativos():
    st.header("Clientes Inativos")
    dados = gerar_dados_clientes_inativos()
    
    fig = px.histogram(dados, x='ultima_compra', title='Distribuição de Inatividade')
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(
        dados.sort_values('ultima_compra').style.format({
            'valor_total': 'R$ {:.2f}',
            'ultima_compra': lambda x: x.strftime("%d/%m/%Y")
        }),
        hide_index=True
    )
    exportar_dados(dados, 'clientes_inativos')

# ========== Main ==========
def main():
    filtros = filtros_sidebar()
    
    menu = {
        "Visão Geral": visao_geral,
        "Análise RFM": lambda: analise_rfm(filtros),
        "Top Produtos": top_produtos,
        "Tendências de Vendas": tendencias_vendas,
        "Clientes Inativos": clientes_inativos
    }
    
    pagina = st.sidebar.radio("Navegação", list(menu.keys()))
    menu[pagina]()

if __name__ == "__main__":
    main()