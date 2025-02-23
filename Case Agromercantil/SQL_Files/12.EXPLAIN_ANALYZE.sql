EXPLAIN ANALYZE
WITH 
PedidosCliente AS (
    SELECT
        pc.id_cliente,
        p.data_pedido,
        p.valor_total  -- Adicionamos o valor_total aqui
    FROM pedido_cliente pc
    JOIN pedidos p ON pc.id_pedido = p.id_pedido
),
UltimoPedido AS (
    SELECT
        id_cliente,
        MAX(data_pedido) AS data_ultimo_pedido
    FROM PedidosCliente
    GROUP BY id_cliente
),
MetricasRFM AS (
    SELECT
        pc.id_cliente,
        CURRENT_DATE - up.data_ultimo_pedido AS dias_desde_ultimo_pedido,
        COUNT(pc.id_cliente) OVER (PARTITION BY pc.id_cliente) AS total_pedidos,
        AVG(pc.valor_total) OVER (PARTITION BY pc.id_cliente) AS ticket_medio  -- Corrigido para pc.valor_total
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