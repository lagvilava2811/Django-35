from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from store import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.HomeView.as_view(), name="home"),
    path("categories/<int:category_id>/", views.CategoryProductsView.as_view(), name="category_products"),
    path("products/add/", views.ProductCreateView.as_view(), name="product_create"),
    path("products/<int:product_id>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:product_id>/edit/", views.ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:product_id>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("sale/", views.SaleProductsView.as_view(), name="sale_products"),
]

if settings.DEBUG:
    urlpatterns = [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns
