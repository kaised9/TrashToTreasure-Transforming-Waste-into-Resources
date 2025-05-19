# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import BuyerProfile, DriverProfile, ArtisanProfile


class CustomUserSignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('driver', 'Delivery Guy'),
        ('artisan', 'Artisan'),
    ]

    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'role', 'password1', 'password2']


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'phone', 'account_status']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),  # Make username read-only
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_status'].disabled = True  # Makes it uneditable in the form

        # Optionally, include DriverProfile fields
        if self.instance.role == 'driver':
            self.fields['delivery_area'] = forms.CharField(max_length=100, required=False)
            self.fields['delivery_count'] = forms.IntegerField(required=False, disabled=True)
            self.fields['order_number'] = forms.IntegerField(required=False, disabled=True)


class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['profile_picture', 'loyalty_points', 'order_number']
        widgets = {
            'loyalty_points': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'order_number': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }
     
        
class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['profile_picture', 'delivery_area', 'delivery_count', 'order_number', 'rating']  # ✅ Add profile_picture
        widgets = {
            'delivery_area': forms.TextInput(attrs={'placeholder': 'Enter delivery area'}),
            'delivery_count': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'order_number': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'rating': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

class ArtisanProfileForm(forms.ModelForm):
    class Meta:
        model = ArtisanProfile
        fields = ['profile_picture', 'bio', 'location']  # include relevant fields only
        widgets = {
            'bio': forms.Textarea(attrs={
                'placeholder': 'Tell us about your craft',
                'rows': 3
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Enter your city/location'
            }),

        }

