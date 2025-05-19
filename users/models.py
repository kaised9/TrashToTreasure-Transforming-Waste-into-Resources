
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.contrib.contenttypes.fields import GenericRelation


# Choices for role and account status
ROLE_CHOICES = (
    ('driver', 'Driver'),
    ('artisan', 'Artisan'),
    ('buyer', 'Buyer'),
)

ACCOUNT_STATUS_CHOICES = (
    ('active', 'Active'),
    ('suspended', 'Suspended'),
    ('deleted', 'Deleted'),
)

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='active')

    objects = CustomUserManager()  # ✅ Use your custom manager
    
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.username} ({self.role})"


# Driver-specific data
class DriverProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    delivery_area = models.CharField(max_length=100, blank=True)
    delivery_count = models.PositiveIntegerField(default=0)
    order_number = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(upload_to='driver_profiles/', null=True, blank=True)
    rating = models.FloatField(default=0.0)
    reviews = GenericRelation('marketplace.Review')
    
    def update_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            avg = round(sum(r.rating for r in ratings) / ratings.count(), 2)
            self.rating = avg
            self.save()

    
    def __str__(self):
        return f"DriverProfile - {self.user.username}"


class DriverRating(models.Model):
    driver   = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='ratings')
    rated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order    = models.ForeignKey('marketplace.Order', on_delete=models.CASCADE, null=True, blank=True)
    rating   = models.PositiveSmallIntegerField()  # 1–5
    comment  = models.TextField(blank=True, null=True)  # optional
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('driver','rated_by','order')  # one rating per driver+buyer+order

    def __str__(self):
        return f"{self.rated_by.username} → {self.driver.user.username} ({self.rating}/5) [Order {self.order.id}]"


# Artisan-specific data
class ArtisanProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='artisan_profiles/', null=True, blank=True)  # Added
    location = models.CharField(max_length=255, blank=True)  # Added
    # Sales Stats
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Added
    product_count = models.PositiveIntegerField(default=0)  # Added: number of products listed
    rating = models.FloatField(default=0.0)  # Added: average rating out of 5
    pending_approval_count = models.PositiveIntegerField(default=0)  # Optional
    order_number = models.PositiveIntegerField(default=0)  # Still keeping this if needed

    def __str__(self):
        return f"ArtisanProfile - {self.user.username}"


# Buyer-specific data
class BuyerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    loyalty_points = models.PositiveIntegerField(default=0)
    order_number = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(upload_to='buyer_profiles/', null=True, blank=True)  # ✅ Add this line
    
    def __str__(self):
        return f"BuyerProfile - {self.user.username}"
