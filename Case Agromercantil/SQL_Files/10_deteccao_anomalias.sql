-- CTE para calcular o valor correto dos pedidos
WITH CalculoCorreto AS (
    SELECT
        p.id_pedido,
        p.valor_total AS valor_total_registrado,
        SUM(i.quantidade * i.preco_unitario) AS valor_calculado
    FROM pedidos p
    JOIN itens_pedido i ON p.id_pedido = i.id_pedido
    GROUP BY p.id_pedido
)
SELECT
    id_pedido,
    valor_total_registrado,
    valor_calculado
FROM CalculoCorreto
WHERE valor_total_registrado != valor_calculado;  -- Filtra discrepâncias