from django.test import TestCase

from product.factories import CategoryFactory, ProductFactory
from product.serializers import ProductSerializer


class TestProductSerializer(TestCase):
    def setUp(self) -> None:
        self.category = CategoryFactory(title="food")
        self.product_1 = ProductFactory(
            title="chicken", price=100, category=[self.category]
        )
        self.product_serializer = ProductSerializer(self.product_1)

    def test_product_serializer(self):
        serializer_data = self.product_serializer.data
        self.assertEqual(serializer_data["price"], 100)
        self.assertEqual(serializer_data["title"], "chicken")
        self.assertEqual(
            serializer_data["category"][0]["title"], "food")