-- Índice para consultas que envolvem a tabela pedido_cliente (ex: RFM, Clientes Inativos)
CREATE INDEX idx_pedido_cliente_cliente ON pedido_cliente(id_cliente);
CREATE INDEX idx_pedido_cliente_pedido ON pedido_cliente(id_pedido);

-- Índice para consultas que filtram por data_pedido (Tendências de Vendas)
CREATE INDEX idx_pedidos_data ON pedidos(data_pedido);

-- Índice para consultas que envolvem itens_pedido (Detecção de Anomalias)
CREATE INDEX idx_itens_pedido_pedido ON itens_pedido(id_pedido);