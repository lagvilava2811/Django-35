from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ProductForm
from .models import Category, Product


class HomeView(TemplateView):
    template_name = "store/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = (
            Product.objects.filter(is_available=True)
            .select_related("category")
            .order_by("price")
        )
        context["categories"] = (
            Category.objects.filter(products__isnull=False)
            .annotate(product_count=Count("products"))
            .distinct()
        )
        return context


class CategoryProductsView(DetailView):
    model = Category
    template_name = "store/category_products.html"
    context_object_name = "category"
    pk_url_kwarg = "category_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.object.products.order_by("price")
        return context


class SaleProductsView(ListView):
    template_name = "store/sale_products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_available=True, has_discount=True).order_by("price")


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"product_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "პროდუქტის დამატება"
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"product_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "პროდუქტის განახლება"
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "store/product_confirm_delete.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"
    success_url = reverse_lazy("home")
