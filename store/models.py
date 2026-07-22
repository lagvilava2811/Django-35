from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    has_discount = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    class Meta:
        db_table = "products"
        ordering = ["price"]

    def __str__(self):
        return f"{self.category} -> {self.name}"
