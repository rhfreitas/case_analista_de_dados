-- CTE para calcular vendas mensais e crescimento percentual
WITH VendasMensais AS (
    SELECT
        TO_CHAR(data_pedido, 'YYYY-MM') AS mes_ano,
        SUM(valor_total) AS total_vendas
    FROM pedidos
    GROUP BY TO_CHAR(data_pedido, 'YYYY-MM')
),
CrescimentoPercentual AS (
    SELECT
        mes_ano,
        total_vendas,
        LAG(total_vendas) OVER (ORDER BY mes_ano) AS vendas_mes_anterior,
        ROUND(
            ((total_vendas - LAG(total_vendas) OVER (ORDER BY mes_ano)) 
            / NULLIF(LAG(total_vendas) OVER (ORDER BY mes_ano), 0) * 100)  -- Parênteses fechado corretamente
        , 2) AS crescimento_percentual  -- Vírgula e casas decimais fora do parêntese interno
    FROM VendasMensais
)
SELECT
    mes_ano,
    total_vendas,
    crescimento_percentual
FROM CrescimentoPercentual
ORDER BY mes_ano;