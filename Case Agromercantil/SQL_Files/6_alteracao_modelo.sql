-- 1. Criar tabela de associação
CREATE TABLE pedido_cliente (
    id_pedido INT REFERENCES pedidos(id_pedido),
    id_cliente INT REFERENCES clientes(id_cliente),
    PRIMARY KEY (id_pedido, id_cliente)  -- Garante combinação única
);

-- 2. Migrar dados existentes (se houver pedidos)
INSERT INTO pedido_cliente (id_pedido, id_cliente)
SELECT id_pedido, id_cliente FROM pedidos;

-- 3. Remover a coluna id_cliente da tabela pedidos
ALTER TABLE pedidos DROP COLUMN id_cliente;