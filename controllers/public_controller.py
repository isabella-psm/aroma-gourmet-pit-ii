from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.repositories import (
    create_order, get_available_product, get_order_by_tracking, get_order_items,
    list_available_products, list_categories,
)

public_bp = Blueprint("public", __name__)


@public_bp.get("/")
def home():
    return render_template("public/home.html", products=list_available_products(), categories=list_categories(), cart_count=cart_count())


def cart_count():
    return sum(session.get("cart", {}).values())


@public_bp.post("/carrinho/adicionar/<int:product_id>")
def add_to_cart(product_id):
    if not get_available_product(product_id):
        flash("Este produto não está disponível no momento.", "error")
        return redirect(url_for("public.home"))
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    flash("Produto adicionado ao pedido.", "success")
    return redirect(request.referrer or url_for("public.cart"))


@public_bp.route("/carrinho", methods=["GET", "POST"])
def cart():
    cart_data = session.get("cart", {})
    if request.method == "POST":
        updated = {}
        for product_id, quantity in cart_data.items():
            try:
                new_quantity = int(request.form.get(f"quantidade_{product_id}", quantity))
            except ValueError:
                new_quantity = quantity
            if new_quantity > 0:
                updated[product_id] = min(new_quantity, 20)
        session["cart"] = updated
        flash("Quantidades atualizadas.", "success")
        return redirect(url_for("public.cart"))

    lines, total = [], 0
    for product_id, quantity in cart_data.items():
        product = get_available_product(int(product_id))
        if product:
            subtotal = product["preco"] * quantity
            lines.append({"product": product, "quantity": quantity, "subtotal": subtotal})
            total += subtotal
    return render_template("public/cart.html", lines=lines, total=total, cart_count=cart_count())


@public_bp.post("/carrinho/remover/<int:product_id>")
def remove_from_cart(product_id):
    cart_data = session.get("cart", {})
    cart_data.pop(str(product_id), None)
    session["cart"] = cart_data
    flash("Produto removido do pedido.", "success")
    return redirect(url_for("public.cart"))


@public_bp.post("/pedido/finalizar")
def checkout():
    tracking_code = create_order(session.get("cart", {}))
    if not tracking_code:
        flash("Seu pedido está vazio ou contém produto indisponível.", "error")
        return redirect(url_for("public.cart"))
    session["cart"] = {}
    return render_template("public/order_success.html", tracking_code=tracking_code)


@public_bp.route("/acompanhar", methods=["GET", "POST"])
def track_order():
    if request.method == "POST":
        code = request.form.get("codigo", "").strip().upper()
        if code:
            return redirect(url_for("public.order_tracking", tracking_code=code))
        flash("Informe o código do pedido.", "error")
    return render_template("public/tracking_search.html")


@public_bp.get("/acompanhar/<tracking_code>")
def order_tracking(tracking_code):
    order = get_order_by_tracking(tracking_code)
    if not order:
        flash("Não encontramos um pedido com esse código.", "error")
        return redirect(url_for("public.track_order"))
    return render_template("public/order_tracking.html", order=order, items=get_order_items(order["id"]))
