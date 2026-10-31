CREATE TABLE IF NOT EXISTS administradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    preco REAL NOT NULL CHECK (preco >= 0),
    imagem_url TEXT NOT NULL,
    disponivel INTEGER NOT NULL DEFAULT 1 CHECK (disponivel IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_acompanhamento TEXT UNIQUE,
    status TEXT NOT NULL DEFAULT 'Recebido' CHECK (status IN ('Recebido', 'Em preparo', 'Pronto', 'Concluído', 'Cancelado')),
    total REAL NOT NULL DEFAULT 0 CHECK (total >= 0),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    produto_nome TEXT NOT NULL,
    preco_unitario REAL NOT NULL CHECK (preco_unitario >= 0),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id) ON DELETE CASCADE
);
