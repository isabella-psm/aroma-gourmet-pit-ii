# Aroma Gourmet - PIT-II

Aplicação web acadêmica de uma cafeteria gourmet. O sistema entrega uma vitrine pública de produtos e um painel administrativo para manter o cardápio. Não há carrinho, pagamentos ou delivery nesta versão, conforme o recorte definido para o PIT-II.

## Requisitos atendidos

- Front-end em HTML, CSS e JavaScript responsivo;
- Back-end em Python com Flask;
- Banco de dados SQLite, inicializado automaticamente;
- Organização MVC: `models/`, `views` (templates) e `controllers/`;
- Carrinho com atualização de quantidades e finalização simples de pedidos;
- Painel administrativo de pedidos, com visualização dos itens e atualização de status;
- Login administrativo, cadastro, edição, exclusão e disponibilidade de produtos;
- Produtos indisponíveis não aparecem no catálogo público;
- Testes automatizados básicos em `tests/test_app.py`.

## Estrutura

```text
cafeteria_gourmet/
├── app.py                    # Criação da aplicação
├── config.py                 # Configurações
├── schema.sql                # Modelo físico do banco
├── controllers/              # Controladores (rotas e regras de entrada)
├── models/                   # Acesso ao SQLite e repositórios
├── templates/                # Views Jinja/HTML
├── static/                   # CSS e JavaScript
├── tests/                    # Testes automatizados
└── docs/                     # Materiais para entrega acadêmica
```

## Como executar

1. Abra um terminal nesta pasta.
2. Crie e ative um ambiente virtual (opcional, mas recomendado):

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instale a dependência e inicie o servidor:

   ```powershell
   py -m pip install -r requirements.txt
   py app.py
   ```

4. Acesse `http://127.0.0.1:5000`.

Por padrão, o projeto mantém SQLite somente como alternativa local de desenvolvimento. Para usar PostgreSQL, suba o serviço definido em `docker-compose.yml`, copie `.env.example` para `.env` e configure `DATABASE_URL` no terminal antes de iniciar a aplicação:

```powershell
docker compose up -d
$env:DATABASE_URL = "postgresql://aroma:aroma@localhost:5432/aroma_gourmet"
py app.py
```

O esquema PostgreSQL é aplicado automaticamente na primeira conexão. A finalização do pedido é demonstrativa: ela não coleta dados pessoais, não processa pagamento e não realiza delivery. O cliente recebe um código para acompanhar somente o status do seu pedido; os demais pedidos permanecem restritos ao administrador. Credenciais de demonstração:

- E-mail: `admin@aromagourmet.local`
- Senha: `admin123`

> Troque a chave secreta e as credenciais em uma eventual publicação real. As imagens, os produtos e os dados desta aplicação são fictícios e servem exclusivamente à demonstração acadêmica.

## Como testar

Com a dependência instalada, execute:

```powershell
py -m unittest discover -s tests -v
```

Além dos testes automatizados, aplique o roteiro de aceitação de `docs/roteiro-testes-colegas.md` com cinco colegas e registre os resultados no modelo `docs/laudo-qualidade-modelo.md`.
