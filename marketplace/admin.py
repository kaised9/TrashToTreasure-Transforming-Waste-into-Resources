from django.contrib import admin
from .models import TrashItem, Review
from .models import TrashItem, UpcycledProduct, Order, OrderItem, CartItem 
from django.contrib.auth import get_user_model
from django import forms

admin.site.register(TrashItem)
admin.site.register(UpcycledProduct)
admin.site.register(OrderItem)
admin.site.register(CartItem)
# Register your models here.

User = get_user_model()

class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(OrderAdminForm, self).__init__(*args, **kwargs)
        # Filter assigned_delivery_guy choices to only drivers
        self.fields['assigned_delivery_guy'].queryset = User.objects.filter(role='driver')

class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm

admin.site.register(Order, OrderAdmin)

admin.site.register(Review)