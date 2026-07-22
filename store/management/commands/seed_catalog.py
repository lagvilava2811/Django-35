from django.core.management.base import BaseCommand

from store.models import Category, Product


class Command(BaseCommand):
    help = "Populate SQLite with categories and products."

    def handle(self, *args, **options):
        categories = {}
        for name in ("Electronics", "Books", "Clothes", "Furniture"):
            categories[name], _ = Category.objects.get_or_create(name=name)

        products = [
            ("MacBook Air", "Electronics", "3299.00", 6, True, True, "Lightweight laptop"),
            ("Apple Watch", "Electronics", "1499.00", 11, True, True, "Smart watch"),
            ("Wireless Headphones", "Electronics", "299.00", 18, True, False, "Noise-cancelling headphones"),
            ("Clean Code", "Books", "85.00", 14, True, True, "A book about writing quality code"),
            ("Django for Beginners", "Books", "70.00", 9, True, False, "Django learning guide"),
            ("Python Crash Course", "Books", "65.00", 12, True, False, "Practical Python introduction"),
            ("Classic T-Shirt", "Clothes", "55.00", 25, True, True, "Cotton T-shirt"),
            ("Denim Jacket", "Clothes", "180.00", 7, True, False, "Blue denim jacket"),
            ("Office Chair", "Furniture", "450.00", 4, True, True, "Ergonomic chair"),
            ("Wooden Desk", "Furniture", "900.00", 3, True, False, "Spacious work desk"),
            ("Old Monitor", "Electronics", "120.00", 0, False, False, "Unavailable monitor"),
        ]
        for name, category_name, price, quantity, available, discount, description in products:
            Product.objects.update_or_create(
                name=name,
                category=categories[category_name],
                defaults={"price": price, "quantity": quantity, "is_available": available, "has_discount": discount, "description": description},
            )
        self.stdout.write(self.style.SUCCESS("Catalog data created."))
