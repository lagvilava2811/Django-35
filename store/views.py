from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def home(request):
    products = Product.objects.filter(is_available=True).order_by("price")
    categories = (
        Category.objects.filter(products__isnull=False)
        .annotate(product_count=Count("products"))
        .distinct()
    )
    return render(request, "store/home.html", {"products": products, "categories": categories})


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_available=True).order_by("price")
    return render(request, "store/category_products.html", {"category": category, "products": products})


def sale_products(request):
    products = Product.objects.filter(is_available=True, has_discount=True).order_by("price")
    return render(request, "store/sale_products.html", {"products": products})
