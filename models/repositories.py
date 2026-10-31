from decimal import Decimal
from secrets import token_hex

from models.database import execute, executemany, get_db


def list_categories():
    return execute("SELECT * FROM categorias ORDER BY nome").fetchall()


def list_available_products():
    return execute(
        """SELECT p.*, c.nome AS categoria_nome FROM produtos p
           JOIN categorias c ON c.id = p.categoria_id
           WHERE p.disponivel IS TRUE ORDER BY c.nome, p.nome"""
    ).fetchall()


def list_all_products():
    return execute(
        """SELECT p.*, c.nome AS categoria_nome FROM produtos p
           JOIN categorias c ON c.id = p.categoria_id ORDER BY c.nome, p.nome"""
    ).fetchall()


def get_product(product_id):
    return execute("SELECT * FROM produtos WHERE id = ?", (product_id,)).fetchone()


def get_available_product(product_id):
    return execute(
        "SELECT * FROM produtos WHERE id = ? AND disponivel IS TRUE", (product_id,)
    ).fetchone()


def create_product(data):
    db = get_db()
    execute(
        """INSERT INTO produtos (nome, categoria_id, descricao, preco, imagem_url, disponivel)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (data["nome"], data["categoria_id"], data["descricao"], data["preco"], data["imagem_url"], bool(data["disponivel"])),
    )
    db.commit()


def update_product(product_id, data):
    db = get_db()
    execute(
        """UPDATE produtos SET nome=?, categoria_id=?, descricao=?, preco=?, imagem_url=?, disponivel=?
           WHERE id=?""",
        (data["nome"], data["categoria_id"], data["descricao"], data["preco"], data["imagem_url"], bool(data["disponivel"]), product_id),
    )
    db.commit()


def delete_product(product_id):
    db = get_db()
    execute("DELETE FROM produtos WHERE id = ?", (product_id,))
    db.commit()


def set_availability(product_id, available):
    db = get_db()
    execute("UPDATE produtos SET disponivel = ? WHERE id = ?", (bool(available), product_id))
    db.commit()


def get_admin_by_email(email):
    return execute("SELECT * FROM administradores WHERE email = ?", (email,)).fetchone()


def create_order(cart):
    """Persist an order from {product_id: quantity}; return its public tracking code."""
    db = get_db()
    items = []
    for product_id, quantity in cart.items():
        product = get_available_product(int(product_id))
        if not product or not isinstance(quantity, int) or quantity < 1:
            return None
        items.append((product, quantity))

    if not items:
        return None

    total = float(sum(Decimal(str(product["preco"])) * quantity for product, quantity in items))
    tracking_code = token_hex(6).upper()
    cursor = execute(
        "INSERT INTO pedidos (codigo_acompanhamento, total) VALUES (?, ?) RETURNING id",
        (tracking_code, total),
    )
    order_id = cursor.fetchone()["id"]
    executemany(
        """INSERT INTO itens_pedido (pedido_id, produto_id, produto_nome, preco_unitario, quantidade)
           VALUES (?, ?, ?, ?, ?)""",
        [(order_id, product["id"], product["nome"], product["preco"], quantity) for product, quantity in items],
    )
    db.commit()
    return tracking_code


def list_orders():
    return execute(
        """SELECT p.*, COUNT(i.id) AS itens
           FROM pedidos p LEFT JOIN itens_pedido i ON i.pedido_id = p.id
           GROUP BY p.id ORDER BY p.id DESC"""
    ).fetchall()


def get_order(order_id):
    return execute("SELECT * FROM pedidos WHERE id = ?", (order_id,)).fetchone()


def get_order_by_tracking(tracking_code):
    return execute(
        "SELECT * FROM pedidos WHERE codigo_acompanhamento = ?", (tracking_code.upper(),)
    ).fetchone()


def get_order_items(order_id):
    return execute(
        "SELECT * FROM itens_pedido WHERE pedido_id = ? ORDER BY id", (order_id,)
    ).fetchall()


def update_order_status(order_id, status):
    db = get_db()
    execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, order_id))
    db.commit()
