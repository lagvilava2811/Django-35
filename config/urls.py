from django.contrib import admin
from django.urls import path

from store import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("categories/<int:category_id>/", views.category_products, name="category_products"),
    path("sale/", views.sale_products, name="sale_products"),
]
