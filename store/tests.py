from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class StoreViewsTests(TestCase):
    def setUp(self):
        self.books = Category.objects.create(name="Books")
        self.empty_category = Category.objects.create(name="Empty")
        self.sale_product = Product.objects.create(
            name="Sale book",
            price=Decimal("20.00"),
            quantity=3,
            category=self.books,
            has_discount=True,
        )
        self.regular_product = Product.objects.create(
            name="Regular book",
            price=Decimal("10.00"),
            quantity=2,
            category=self.books,
        )
        Product.objects.create(
            name="Unavailable book",
            price=Decimal("5.00"),
            quantity=0,
            category=self.books,
            is_available=False,
        )

    def test_home_shows_available_products_by_price_and_non_empty_categories(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["products"],
            [self.regular_product, self.sale_product],
            ordered=True,
        )
        categories = response.context["categories"]
        self.assertEqual(list(categories), [self.books])
        self.assertEqual(categories[0].product_count, 3)
        self.assertContains(response, "SALE")

    def test_category_sale_and_product_detail_pages_render(self):
        urls = [
            reverse("category_products", args=[self.books.id]),
            reverse("sale_products"),
            reverse("product_detail", args=[self.sale_product.id]),
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)
