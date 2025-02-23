-- Análise RFM com CTE e funções de janela
WITH 
PedidosCliente AS (
    SELECT
        id_cliente,
        data_pedido,
        valor_total,
        -- Usando LAG para pegar a data do pedido anterior do mesmo cliente
        LAG(data_pedido) OVER (PARTITION BY id_cliente ORDER BY data_pedido) AS data_pedido_anterior
    FROM pedidos
),
UltimoPedido AS (
    SELECT
        id_cliente,
        MAX(data_pedido) AS data_ultimo_pedido
    FROM pedidos
    GROUP BY id_cliente
),
MetricasRFM AS (
    SELECT
        pc.id_cliente,
        -- Recência (dias desde o último pedido)
        CURRENT_DATE - up.data_ultimo_pedido AS dias_desde_ultimo_pedido,
        -- Frequência (total de pedidos)
        COUNT(pc.id_cliente) OVER (PARTITION BY pc.id_cliente) AS total_pedidos,
        -- Valor (ticket médio)
        AVG(pc.valor_total) OVER (PARTITION BY pc.id_cliente) AS ticket_medio
    FROM PedidosCliente pc
    JOIN UltimoPedido up ON pc.id_cliente = up.id_cliente
)
SELECT DISTINCT 
    id_cliente,
    dias_desde_ultimo_pedido,
    total_pedidos,
    ROUND(ticket_medio::numeric, 2) AS ticket_medio
FROM MetricasRFM
ORDER BY dias_desde_ultimo_pedido DESC;