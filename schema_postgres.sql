CREATE TABLE IF NOT EXISTS administradores (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categorias (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS produtos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria_id BIGINT NOT NULL REFERENCES categorias(id),
    descricao TEXT NOT NULL,
    preco NUMERIC(10, 2) NOT NULL CHECK (preco >= 0),
    imagem_url TEXT NOT NULL,
    disponivel BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pedidos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo_acompanhamento VARCHAR(12) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'Recebido' CHECK (status IN ('Recebido', 'Em preparo', 'Pronto', 'Concluído', 'Cancelado')),
    total NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (total >= 0),
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS itens_pedido (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pedido_id BIGINT NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    produto_id BIGINT NOT NULL,
    produto_nome TEXT NOT NULL,
    preco_unitario NUMERIC(10, 2) NOT NULL CHECK (preco_unitario >= 0),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0)
);
