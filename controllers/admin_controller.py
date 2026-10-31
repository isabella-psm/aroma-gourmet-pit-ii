from functools import wraps
from decimal import Decimal, InvalidOperation

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, abort
from werkzeug.security import check_password_hash

from models.repositories import (
    create_product, delete_product, get_admin_by_email, get_product, list_all_products,
    list_categories, set_availability, update_product, get_order, get_order_items, list_orders,
    update_order_status,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "admin_id" not in session:
            flash("Entre para acessar o painel administrativo.", "error")
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)
    return wrapped_view


def form_data(form):
    name = form.get("nome", "").strip()
    description = form.get("descricao", "").strip()
    image_url = form.get("imagem_url", "").strip()
    try:
        category_id = int(form.get("categoria_id", ""))
        price = Decimal(form.get("preco", "").replace(",", "."))
        if not name or not description or not image_url or price < 0:
            raise ValueError
    except (ValueError, InvalidOperation):
        return None
    return {"nome": name, "categoria_id": category_id, "descricao": description,
            "preco": float(price), "imagem_url": image_url,
            "disponivel": 1 if form.get("disponivel") else 0}


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        admin = get_admin_by_email(request.form.get("email", "").strip().lower())
        if admin and check_password_hash(admin["senha_hash"], request.form.get("senha", "")):
            session.clear()
            session["admin_id"] = admin["id"]
            session["admin_name"] = admin["nome"]
            return redirect(url_for("admin.dashboard"))
        flash("E-mail ou senha inválidos.", "error")
    return render_template("admin/login.html")


@admin_bp.get("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada.", "success")
    return redirect(url_for("public.home"))


@admin_bp.get("/")
@login_required
def dashboard():
    return render_template("admin/dashboard.html", products=list_all_products())


@admin_bp.get("/pedidos")
@login_required
def orders():
    return render_template("admin/orders.html", orders=list_orders())


@admin_bp.get("/pedidos/<int:order_id>")
@login_required
def order_detail(order_id):
    order = get_order(order_id)
    if not order:
        abort(404)
    return render_template("admin/order_detail.html", order=order, items=get_order_items(order_id))


@admin_bp.post("/pedidos/<int:order_id>/status")
@login_required
def change_order_status(order_id):
    if not get_order(order_id):
        abort(404)
    status = request.form.get("status", "")
    if status in {"Recebido", "Em preparo", "Pronto", "Concluído", "Cancelado"}:
        update_order_status(order_id, status)
        flash("Status do pedido atualizado.", "success")
    else:
        flash("Status inválido.", "error")
    return redirect(url_for("admin.order_detail", order_id=order_id))


@admin_bp.route("/produtos/novo", methods=["GET", "POST"])
@login_required
def new_product():
    if request.method == "POST":
        data = form_data(request.form)
        if data:
            create_product(data)
            flash("Produto cadastrado com sucesso.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Preencha todos os campos com valores válidos.", "error")
    return render_template("admin/product_form.html", product=None, categories=list_categories())


@admin_bp.route("/produtos/<int:product_id>/editar", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = get_product(product_id)
    if not product:
        abort(404)
    if request.method == "POST":
        data = form_data(request.form)
        if data:
            update_product(product_id, data)
            flash("Produto atualizado com sucesso.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Preencha todos os campos com valores válidos.", "error")
    return render_template("admin/product_form.html", product=product, categories=list_categories())


@admin_bp.post("/produtos/<int:product_id>/excluir")
@login_required
def remove_product(product_id):
    delete_product(product_id)
    flash("Produto excluído.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.post("/produtos/<int:product_id>/disponibilidade")
@login_required
def toggle_availability(product_id):
    product = get_product(product_id)
    if not product:
        abort(404)
    set_availability(product_id, 0 if product["disponivel"] else 1)
    flash("Disponibilidade atualizada.", "success")
    return redirect(url_for("admin.dashboard"))
