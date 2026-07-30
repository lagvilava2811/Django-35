from decimal import Decimal

from django.test import TestCase
from django.conf import settings
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

    def test_home_loads_products_and_categories_in_two_queries(self):
        with self.assertNumQueries(2):
            self.client.get(reverse("home"))

    def test_debug_toolbar_is_enabled(self):
        self.assertIn("debug_toolbar", settings.INSTALLED_APPS)


class ProductManagementTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Headphones",
            price=Decimal("99.99"),
            quantity=5,
            category=self.category,
        )

    def test_create_product(self):
        response = self.client.post(
            reverse("product_create"),
            {
                "name": "Keyboard",
                "price": "149.99",
                "quantity": 8,
                "description": "Mechanical keyboard",
                "is_available": "on",
                "has_discount": "on",
                "category": self.category.id,
            },
        )

        product = Product.objects.get(name="Keyboard")
        self.assertRedirects(response, reverse("product_detail", args=[product.id]))
        self.assertTrue(product.has_discount)

    def test_update_product(self):
        response = self.client.post(
            reverse("product_update", args=[self.product.id]),
            {
                "name": "Updated headphones",
                "price": "79.99",
                "quantity": 7,
                "description": "Updated description",
                "is_available": "on",
                "category": self.category.id,
            },
        )

        self.product.refresh_from_db()
        self.assertRedirects(response, reverse("product_detail", args=[self.product.id]))
        self.assertEqual(self.product.name, "Updated headphones")
        self.assertEqual(self.product.price, Decimal("79.99"))
        self.assertFalse(self.product.has_discount)

    def test_delete_product_requires_confirmation_and_removes_product(self):
        url = reverse("product_delete", args=[self.product.id])

        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(url)

        self.assertRedirects(response, reverse("home"))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
