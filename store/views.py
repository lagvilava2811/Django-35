from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Category, Product


def home(request):
    products = Product.objects.filter(is_available=True).select_related("category").order_by("price")
    categories = (
        Category.objects.filter(products__isnull=False)
        .annotate(product_count=Count("products"))
        .distinct()
    )
    return render(request, "store/home.html", {"products": products, "categories": categories})


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).order_by("price")
    return render(request, "store/category_products.html", {"category": category, "products": products})


def sale_products(request):
    products = Product.objects.filter(is_available=True, has_discount=True).order_by("price")
    return render(request, "store/sale_products.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "store/product_detail.html", {"product": product})


def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        product = form.save()
        return redirect("product_detail", product_id=product.id)
    return render(request, "store/product_form.html", {"form": form, "title": "პროდუქტის დამატება"})


def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        product = form.save()
        return redirect("product_detail", product_id=product.id)
    return render(
        request,
        "store/product_form.html",
        {"form": form, "title": "პროდუქტის განახლება", "product": product},
    )


def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect("home")
    return render(request, "store/product_confirm_delete.html", {"product": product})
