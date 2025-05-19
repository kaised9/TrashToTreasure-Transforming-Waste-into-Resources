from django import forms
from .models import UpcycledProduct

class UpcycledProductForm(forms.ModelForm):
    class Meta:
        model = UpcycledProduct
        # only expose the fields the artisan actually fills in:
        fields = [
            'product_name',
            'category',
            'description',
            'price',
            'stock_availability',
            'product_images',
            'location',
            'tags',
        ]
