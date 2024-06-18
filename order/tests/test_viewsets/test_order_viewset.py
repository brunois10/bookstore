import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from order.factories import OrderFactory, UserFactory
from order.models.order import Order
from product.factories import CategoryFactory, ProductFactory


class TestOrderViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        self.client = APIClient()
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category]
        )
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertIsInstance(order_data, list)  # Verifica se é uma lista de objetos JSON

        # Verifica se há exatamente 1 objeto na lista
        self.assertEqual(len(order_data), 1)
        order_obj = order_data[0]

        # Verifica os dados da ordem
        self.assertIn("product", order_obj)
        products = order_obj["product"]
        self.assertEqual(len(products), 1)  # Verifica se há exatamente 1 produto associado à ordem

        product = products[0]
        self.assertEqual(product["title"], self.product.title)
        self.assertEqual(int(product["price"]), self.product.price)  # Convertendo para inteiro aqui
        self.assertEqual(product["active"], self.product.active)

        # Verifica os dados da categoria do produto
        self.assertIn("category", product)
        categories = product["category"]
        self.assertEqual(len(categories), 1)  # Verifica se há exatamente 1 categoria associada ao produto

        category = categories[0]
        self.assertEqual(category["title"], self.category.title)

        # Verifica outros dados da ordem
        self.assertIn("total", order_obj)
        self.assertIn("user", order_obj)

        # Verifica se o ID do usuário está correto
        self.assertEqual(order_obj["user"], self.order.user.id)

    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        data = json.dumps({"products_id": [product.id], "user": user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)