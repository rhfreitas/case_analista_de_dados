# Case Técnico - Analista de Dados 🚀

**Objetivo:** Resolução de um case técnico para vaga de Analista de Dados, envolvendo PostgreSQL, Python (Streamlit) e análise exploratória.  
**Contexto:** Simulação de um e-commerce fictício com foco em vendas, segmentação de clientes (RFM), detecção de anomalias e otimização de consultas.

---

## 📂 Estrutura do Projeto
Case Agromercantil/
├── SQL_Files/
│ ├── 5_rfm_completo.sql # Análise RFM
│ ├── 6_alteracao_modelo.sql # Modelo para pedidos compartilhados
│ ├── 8_tendencias_vendas.sql # Tendências de vendas mensais
│ ├── 9_clientes_inativos.sql # Clientes inativos (últimos 6 meses)
│ ├── 10_deteccao_anomalias.sql # Detecção de divergências em pedidos
│ ├── 11_otimizacao.sql # Criação de índices de otimização
│ └── 12.EXPLAIN_ANALYZE.sql # Análise de performance
├── meu_dashboard/
│ ├── dashboard.py # Aplicação Streamlit (visualizações)
│ └── analise_exploratoria.py # Análise estatística e gráficos
├── Prints/
│ ├── 1_clientes.png # Tabela de clientes
│ ├── 6_rfm_resultado_final.png # Resultado RFM
│ ├── top5_produtos_receita.png # Produtos mais rentáveis
│ ├── tendencia_de_vendas.png # Gráfico de tendências
│ ├── clientes_inativos.png # Lista de clientes inativos
│ └── visao_geral_streamlit.png # Dashboard interativo
└── ReadMe.txt # Documentação (este arquivo)

Copy

---

## Principais Tarefas Resolvidas

### 1. Inserção de Dados e Validação  
**Arquivos:**  
- Scripts de criação de tabelas e inserção manual (via PostgreSQL).  
- **Prints:** `1_clientes.png`, `2_produtos.png`, `3_pedidos.png`, `4_itens_pedido.png`.  
**Justificativa:** Dados gerados incluem clientes ativos/inativos, produtos de categorias variadas (eletrônicos, vestuário) e pedidos com valores discrepantes para testar anomalias.

---

### 2. Análise RFM (Recência, Frequência, Valor)  
**Consulta SQL:** `5_rfm_completo.sql`  
**Resultado:**  
- `dias_desde_ultimo_pedido` calculado com `LAG`, `total_pedidos` via `COUNT OVER`, e `ticket_medio` com `AVG`.  
**Visualização:** `6_rfm_resultado_final.png` (clientes segmentados por comportamento).

---

### 3. Alteração do Modelo para Pedidos Compartilhados  
**Solução:** Criação de tabela de associação `pedido_cliente` (relação N:N).  
**Arquivo:** `6_alteracao_modelo.sql`  
**Print:** `7_alteracao_modelo_resultado.png` (exemplo de pedido com múltiplos clientes).

---

### 4. Top 5 Produtos Mais Rentáveis (Último Ano)  
**Consulta:** CTE com cálculo de `SUM(quantidade * preco_unitario)`.  
**Visualização:** `top5_produtos_receita.png` (ranking por receita total).

---

### 5. Análise de Tendências de Vendas Mensais  
**Técnica:** Uso de `LAG` para comparar crescimento percentual entre meses.  
**Print:** `tendencia_de_vendas.png` (gráfico de linhas com variação).

---

### 6. Detecção de Anomalias em Pedidos  
**Consulta:** Comparação entre `valor_total` e soma de `quantidade * preco_unitario`.  
**Resultado:** `10_anomalias_resultado.png` (pedidos com divergências).

---

### 7. Otimização e Indexação  
**Índices Criados:**  
- `idx_pedidos_data` (acelera filtros por data).  
- `idx_itens_pedido_pedido` (melhora JOINs em agregações).  
**Análise:** `11_explain_rfm.png` (resultado do `EXPLAIN ANALYZE`).

---

## Dashboard Interativo (Streamlit)  
**Funcionalidades:**  
- Filtros por período, cliente e categoria.  
- Gráficos de tendências, tabelas RFM e top produtos.  
**Arquivos:** `dashboard.py`, `analise_exploratoria.py`  
**Visualização:** `visao_geral_streamlit.png`.

---

## Como Executar o Projeto  
1. **Banco de Dados:** Execute os scripts SQL em ordem (via PostgreSQL).  
2. **Streamlit:** Instale as dependências (`streamlit`, `pandas`, `matplotlib`) e execute:  
```bash
streamlit run meu_dashboard/dashboard.py
📊 Tecnologias Utilizadas
Banco de Dados: PostgreSQL

Visualização: Python (Streamlit, Pandas, Matplotlib)

Versionamento: GitHub

Critérios de Avaliação:
✅ Clareza e estruturação do código
✅ Uso eficiente de CTEs e funções de janela
✅ Visualizações interativas e justificativas técnicas
✅ Documentação completa e reproduzível.


--- 
**Dúvidas?** Consulte os arquivos SQL e os prints na pasta `Prints` para detalhes adicionais!
