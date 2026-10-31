import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from models.database import get_db


class CafeAppTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app({"TESTING": True, "SECRET_KEY": "test", "DATABASE": os.path.join(self.temp_dir.name, "test.db")})
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def login(self):
        return self.client.post("/admin/login", data={"email": "admin@aromagourmet.local", "senha": "admin123"}, follow_redirects=True)

    def test_public_menu_displays_seeded_products(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Espresso Intenso", response.get_data(as_text=True))

    def test_dashboard_requires_login(self):
        response = self.client.get("/admin/", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login", response.headers["Location"])

    def test_admin_can_create_product_and_it_is_public(self):
        self.login()
        response = self.client.post("/admin/produtos/novo", data={
            "nome": "Chá de Frutas", "categoria_id": "1", "descricao": "Bebida de demonstração.",
            "preco": "11.50", "imagem_url": "https://example.com/cha.jpg", "disponivel": "on",
        }, follow_redirects=True)
        self.assertIn("Produto cadastrado com sucesso", response.get_data(as_text=True))
        self.assertIn("Chá de Frutas", self.client.get("/").get_data(as_text=True))

    def test_unavailable_product_is_hidden_from_public_menu(self):
        self.login()
        response = self.client.post("/admin/produtos/1/disponibilidade", follow_redirects=True)
        self.assertIn("Disponibilidade atualizada", response.get_data(as_text=True))
        self.assertNotIn("Espresso Intenso", self.client.get("/").get_data(as_text=True))

    def test_customer_can_finish_order_and_admin_can_view_it(self):
        self.client.post("/carrinho/adicionar/1", follow_redirects=True)
        response = self.client.post("/pedido/finalizar", follow_redirects=True)
        self.assertIn("Pedido recebido", response.get_data(as_text=True))
        self.assertIn("Acompanhar pedido", response.get_data(as_text=True))
        with self.app.app_context():
            code = get_db().execute("SELECT codigo_acompanhamento FROM pedidos WHERE id = 1").fetchone()[0]
        tracking = self.client.get(f"/acompanhar/{code}")
        self.assertIn("Status atual", tracking.get_data(as_text=True))
        self.login()
        orders = self.client.get("/admin/pedidos")
        self.assertIn("#1", orders.get_data(as_text=True))
        detail = self.client.get("/admin/pedidos/1")
        self.assertIn("Espresso Intenso", detail.get_data(as_text=True))

    def test_cart_quantity_can_be_updated(self):
        self.client.post("/carrinho/adicionar/1")
        response = self.client.post("/carrinho", data={"quantidade_1": "3"}, follow_redirects=True)
        self.assertIn("R$ 25,50", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
