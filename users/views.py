from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserSignupForm
from .models import DriverProfile, ArtisanProfile, BuyerProfile
from django.contrib.auth.decorators import login_required
from .forms import BuyerProfileForm, CustomUserForm, DriverProfileForm
from .models import DriverRating
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from .forms import ArtisanProfileForm  # Make sure this import is added at the top


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # ✅ Create profile based on role
            if user.role == 'buyer':
                BuyerProfile.objects.create(user=user)
            elif user.role == 'driver':
                DriverProfile.objects.create(user=user)
            elif user.role == 'artisan':
                ArtisanProfile.objects.create(user=user)

            messages.success(request, 'Signup successful. Please log in.')
            return redirect('login')
    else:
        form = CustomUserSignupForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def buyer_profile(request):
    if request.user.role != 'buyer':
        return redirect('home')  # Block access if not a buyer

    buyer_profile = request.user.buyerprofile
    user_form = CustomUserForm(instance=request.user)
    profile_form = BuyerProfileForm(instance=buyer_profile)

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=request.user)
        profile_form = BuyerProfileForm(request.POST, request.FILES, instance=buyer_profile)  # ← Fixed here

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('buyer_profile')  # Refresh the page

    return render(request, 'buyer_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
    
@login_required
def artisan_profile(request):
    if request.user.role != 'artisan':
        return redirect('home')  # Block access if not an artisan

    artisan_profile_instance = request.user.artisanprofile
    user_form = CustomUserForm(instance=request.user)
    profile_form = ArtisanProfileForm(instance=artisan_profile_instance)

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=request.user)
        profile_form = ArtisanProfileForm(request.POST, request.FILES, instance=artisan_profile_instance)

        if user_form.is_valid() and profile_form.is_valid():
            print("Saving user form:", user_form.cleaned_data)
            print("Saving artisan profile form:", profile_form.cleaned_data)
            user_form.save()
            profile_form.save()
            return redirect('artisan_profile')  # Refresh the page
        else:
            print("User form errors:", user_form.errors)
            print("Artisan profile form errors:", profile_form.errors)

    return render(request, 'artisan_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required    
def driver_profile(request):
    if request.user.role != 'driver':
        return redirect('driver_dashboard')  # Block access if not a driver

    driver_profile = request.user.driverprofile
    user_form = CustomUserForm(instance=request.user)
    profile_form = DriverProfileForm(instance=driver_profile)

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=request.user)
        profile_form = DriverProfileForm(request.POST, request.FILES, instance=driver_profile)

        #if user_form.is_valid() and profile_form.is_valid():
        #    user_form.save()
        #    profile_form.save()
        #    return redirect('driver_profile')  # Refresh the page
        
        if user_form.is_valid() and profile_form.is_valid():
            print("Saving user form:", user_form.cleaned_data)
            print("Saving profile form:", profile_form.cleaned_data)
            user_form.save()
            profile_form.save()
            return redirect('driver_profile')
        else:
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)


    return render(request, 'driver_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
    

@login_required
def rate_driver(request, driver_id):
    driver_profile = get_object_or_404(DriverProfile, id=driver_id)

    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        review_text = request.POST.get('review', '')

        DriverRating.objects.create(
            driver=driver_profile,
            rated_by=request.user,
            rating=rating_value,
            review=review_text
        )

        # ✅ Update average rating
        avg_rating = DriverRating.objects.filter(driver=driver_profile).aggregate(Avg('rating'))['rating__avg'] or 0
        driver_profile.rating = round(avg_rating, 1)
        driver_profile.save()

        messages.success(request, "Rating submitted successfully.")
        return redirect('home')  # Or wherever makes sense

    return render(request, 'rate_driver.html', {'driver': driver_profile})
