from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
import uuid 
from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Avg

User = get_user_model()


class Review(models.Model):
    reviewer        = models.ForeignKey(User, on_delete=models.CASCADE)
    rating          = models.PositiveSmallIntegerField()              # 1–5
    comment         = models.TextField(blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    # Generic relation to either a product or a driver
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('reviewer', 'content_type', 'object_id')  # one review per user+target

    def __str__(self):
        return f"{self.reviewer} → {self.content_object} ({self.rating}/5)"


# Choices for condition, status, and delivery state
CONDITION_CHOICES = [
    ('new', 'New'),
    ('used', 'Used'),
    ('damaged', 'Damaged'),
]

PRODUCT_STATUS_CHOICES = [
    ('active', 'Active'),
    ('sold_out', 'Sold Out'),
    ('inactive', 'Inactive'),
]

DELIVERY_STATUS_CHOICES = [
    ('ready', 'Ready'),
    ('packed', 'Packed'),
    ('on_the_way', 'On its way'),
    ('delivered', 'Delivered'),
]

# Waste Materials Model
class TrashItem(models.Model):
    #product_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    material_name = models.CharField(max_length=255, default="")  # Change as needed
    category = models.CharField(max_length=100, default="")  # Change as needed
    description = models.TextField()
    condition = models.CharField(max_length=50, default="")  # Set a meaningful default
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    trash_point = models.CharField(max_length=255, default="")  # Set a meaningful default
    images = models.ImageField(upload_to='waste_images/', blank=True, null=True)
    location = models.CharField(max_length=255, default="")  # Set a meaningful default
    product_status = models.CharField(max_length=20, choices=PRODUCT_STATUS_CHOICES, default='')
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='')

    # New fields
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    listing_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    reviews = GenericRelation(Review)
    
    def update_average_rating(self):
        avg_rating = self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0
        self.rating = round(avg_rating, 2)
        self.save(update_fields=['rating'])
    
    def __str__(self):
        return f"{self.material_name} - {self.trash_point}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.material_name}-{self.trash_point}")
        super().save(*args, **kwargs)


# Upcycled Products Model
class UpcycledProduct(models.Model):
    product_name = models.CharField(max_length=255, default="")
    category = models.CharField(max_length=100, default="")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_status = models.CharField(max_length=20, choices=PRODUCT_STATUS_CHOICES, default='active')
    
    # Replacing name/contact with a ForeignKey to Artisan user
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upcycled_products', null=True, blank=True)

    approval_status = models.BooleanField(default=False)
    stock_availability = models.IntegerField()
    product_images = models.ImageField(upload_to='upcycled_products/', blank=True, null=True)
    location = models.CharField(max_length=255, default="")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    tags = models.CharField(max_length=255, blank=True, null=True)
    listing_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    sold_count = models.IntegerField(default=0)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='ready')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    reviews = GenericRelation(Review)
    
    def update_average_rating(self):
        avg_rating = self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0
        self.rating = round(avg_rating, 2)
        self.save(update_fields=['rating'])

    def __str__(self):
        if self.artisan:
            # use the custom name field
          display_name = getattr(self.artisan, 'name', None) or self.artisan.get_full_name() or self.artisan.username
        else:
            display_name = "Unknown"
        return f"{self.product_name} by {display_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            artisan_username = self.artisan.username if self.artisan else 'unknown-artisan'
            self.slug = slugify(f"{self.product_name}-{artisan_username}")
        super().save(*args, **kwargs)

class CartItem(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    # Generic link to any product-type model (UpcycledProduct, TrashMaterial, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'content_type', 'object_id')

    def subtotal(self):
        return self.quantity * self.item.price  # works as long as both models have a .price
    
    
    
class Order(models.Model):
    PAYMENT_CHOICES = [
        ('sslcommerz', 'SSLCommerz'),
        ('cod', 'Cash on Delivery'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    
    DELIVERY_STATUS_CHOICES = [
        ('ready', 'Ready to Ship'),
        ('packed', 'Packed'),
        ('on_the_way', 'On the Way'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')  
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='ready')  
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_delivery_guy = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_orders'
    )
    expected_delivery = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
