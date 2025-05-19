from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    content_object = instance.content_object
    if hasattr(content_object, 'update_average_rating'):
        content_object.update_average_rating()

# signals.py


@receiver(post_save, sender=Order)
def handle_paid_order(sender, instance, **kwargs):
    if instance.payment_status == 'paid':
        for item in instance.items.all():
            product = item.content_type.get_object_for_this_type(id=item.object_id)

            if hasattr(product, 'sold_count') and hasattr(product, 'stock_availability'):
                product.sold_count += item.quantity
                product.stock_availability -= item.quantity
                product.save()
            elif hasattr(product, 'quantity'):
                product.quantity -= item.quantity
                product.save()
