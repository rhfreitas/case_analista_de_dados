-- CTE para identificar clientes inativos
WITH UltimoPedido AS (
    SELECT
        pc.id_cliente,
        MAX(p.data_pedido) AS data_ultimo_pedido  -- Última data de pedido do cliente
    FROM pedido_cliente pc
    JOIN pedidos p ON pc.id_pedido = p.id_pedido  -- Junção com a tabela de pedidos
    GROUP BY pc.id_cliente
)
SELECT
    c.id_cliente,
    c.nome,
    up.data_ultimo_pedido,
    CURRENT_DATE - up.data_ultimo_pedido AS dias_inatividade
FROM clientes c
LEFT JOIN UltimoPedido up ON c.id_cliente = up.id_cliente
WHERE 
    up.data_ultimo_pedido < CURRENT_DATE - INTERVAL '6 months'  -- Mais de 6 meses
    OR up.data_ultimo_pedido IS NULL;  -- Clientes sem pedidos