from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "price",
            "quantity",
            "description",
            "is_available",
            "has_discount",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
