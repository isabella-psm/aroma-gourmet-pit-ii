# Síntese de requisitos do PIT-II

## Contexto e recorte

O PIT-I planejou uma loja virtual de cafeteria gourmet. Para o PIT-II, o escopo foi organizado em catálogo público, carrinho de pedidos e administração de produtos e pedidos. Pagamento e delivery ficam explicitamente fora desta versão.

## Requisitos funcionais

1. Exibir apresentação da cafeteria, categorias e cardápio público.
2. Exibir nome, descrição, preço e imagem dos produtos disponíveis.
3. Permitir que o administrador se autentique.
4. Permitir listar, cadastrar, editar e excluir produtos.
5. Permitir marcar cada produto como disponível ou indisponível.
6. Refletir as alterações administrativas no catálogo público.
7. Permitir incluir produtos em um carrinho, alterar quantidades e finalizar um pedido demonstrativo.
8. Permitir que o administrador visualize itens dos pedidos e atualize seu status.

## Requisitos não funcionais

- Interface clara, consistente, responsiva e com feedback das ações.
- Arquitetura MVC e banco relacional SQLite.
- Dados de demonstração sem informações pessoais.
- Código executável, documentado e acompanhado de testes.

## Modelo físico resumido

| Tabela | Finalidade | Campos principais |
|---|---|---|
| `administradores` | Autenticação administrativa | id, nome, email, senha_hash |
| `categorias` | Organização do cardápio | id, nome, descricao |
| `produtos` | Itens exibidos e administrados | id, nome, categoria_id, descricao, preco, imagem_url, disponivel |
| `pedidos` | Pedidos demonstrativos registrados | id, status, total, criado_em |
| `itens_pedido` | Produtos e quantidades de cada pedido | id, pedido_id, produto_id, produto_nome, preco_unitario, quantidade |

Relações: uma categoria possui vários produtos; cada produto pertence a uma categoria; um pedido possui um ou mais itens de pedido.

## Roteiro sugerido para o vídeo (até 5 minutos)

1. Apresente o objetivo e o recorte do projeto (30 s).
2. Navegue na página pública e use os filtros de categoria (1 min).
3. Faça login e explique o painel (40 s).
4. Cadastre ou edite um produto e altere sua disponibilidade (1 min 30 s).
5. Volte ao cardápio e prove que a alteração foi refletida (40 s).
6. Mostre os testes, laudos e melhorias registradas (40 s).
