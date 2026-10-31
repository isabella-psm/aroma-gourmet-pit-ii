import sqlite3
from pathlib import Path

from flask import current_app, g
from werkzeug.security import generate_password_hash


SCHEMA_DIR = Path(__file__).resolve().parent.parent


def using_postgres():
    return bool(current_app.config.get("DATABASE_URL"))


def get_db():
    if "db" not in g:
        if using_postgres():
            import psycopg
            from psycopg.rows import dict_row
            g.db = psycopg.connect(current_app.config["DATABASE_URL"], row_factory=dict_row)
        else:
            g.db = sqlite3.connect(current_app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def execute(query, params=()):
    """Run parameterized SQL on SQLite (tests) or PostgreSQL (application)."""
    if using_postgres():
        query = query.replace("?", "%s")
    return get_db().execute(query, params)


def executemany(query, params):
    if using_postgres():
        query = query.replace("?", "%s")
    return get_db().executemany(query, params)


def init_app(app):
    app.teardown_appcontext(close_db)


def initialize_database():
    if not using_postgres():
        database_path = Path(current_app.config["DATABASE"])
        database_path.parent.mkdir(exist_ok=True)
    db = get_db()
    schema_name = "schema_postgres.sql" if using_postgres() else "schema.sql"
    schema = (SCHEMA_DIR / schema_name).read_text(encoding="utf-8")
    if using_postgres():
        for statement in schema.split(";"):
            if statement.strip():
                db.execute(statement)
    else:
        db.executescript(schema)

    # Compatibilidade para bancos SQLite criados antes do rastreio de pedidos.
    if not using_postgres():
        order_columns = {row["name"] for row in db.execute("PRAGMA table_info(pedidos)").fetchall()}
        if "codigo_acompanhamento" not in order_columns:
            db.execute("ALTER TABLE pedidos ADD COLUMN codigo_acompanhamento TEXT")
            db.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_pedidos_codigo ON pedidos(codigo_acompanhamento)")

    if execute("SELECT COUNT(*) AS total FROM administradores").fetchone()["total"] == 0:
        execute(
            "INSERT INTO administradores (nome, email, senha_hash) VALUES (?, ?, ?)",
            ("Administrador", "admin@aromagourmet.local", generate_password_hash("admin123")),
        )

    if execute("SELECT COUNT(*) AS total FROM categorias").fetchone()["total"] == 0:
        executemany(
            "INSERT INTO categorias (nome, descricao) VALUES (?, ?)",
            [
                ("Cafés", "Bebidas preparadas com grãos selecionados."),
                ("Especiais", "Receitas autorais para momentos especiais."),
                ("Acompanhamentos", "Doces e salgados feitos para combinar com café."),
            ],
        )

    if execute("SELECT COUNT(*) AS total FROM produtos").fetchone()["total"] == 0:
        categories = {row["nome"]: row["id"] for row in execute("SELECT id, nome FROM categorias")}
        products = [
            ("Espresso Intenso", "Cafés", "Café encorpado, extraído na hora, com notas de cacau.", 8.50, "https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?auto=format&fit=crop&w=900&q=80"),
            ("Cappuccino da Casa", "Cafés", "Espresso, leite vaporizado e chocolate em pó artesanal.", 14.90, "https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&w=900&q=80"),
            ("Mocha Avelã", "Especiais", "Café, chocolate cremoso e toque delicado de avelã.", 17.90, "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?auto=format&fit=crop&w=900&q=80"),
            ("Cold Brew Cítrico", "Especiais", "Infusão fria de café com laranja e água tônica.", 16.50, "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=80"),
            ("Croissant de Manteiga", "Acompanhamentos", "Massa folhada assada diariamente, leve e dourada.", 12.00, "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80"),
            ("Brownie 70% Cacau", "Acompanhamentos", "Brownie macio de chocolate intenso e nozes.", 13.50, "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=80"),
        ]
        executemany(
            """INSERT INTO produtos (nome, categoria_id, descricao, preco, imagem_url, disponivel)
               VALUES (?, ?, ?, ?, ?, TRUE)""",
            [(name, categories[category], description, price, image) for name, category, description, price, image in products],
        )
    db.commit()
