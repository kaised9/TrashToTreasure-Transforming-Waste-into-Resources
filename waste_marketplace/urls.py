"""
URL configuration for waste_marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from marketplace.views import login_view, home, checkout
from marketplace.views import driver_dashboard, contact, cart, about, product_listing
from users.views import signup_view, buyer_profile, artisan_profile, driver_profile, driver_profile
from marketplace.views import logout_view  # Assuming you have a logout view
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from marketplace.views import listed_products, order_history  # Assuming you have a view for listed products
from marketplace import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),  # Assuming you have a logout view
    path('signup/', signup_view, name='signup'),  
    path('', home, name='home'),  
    path('driver_dashboard/', driver_dashboard, name='driver_dashboard'),
    path('cart/', cart, name='cart'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('product_listing/', product_listing, name='product_listing'),
    path('checkout/', checkout, name='checkout'),
    path('buyer_profile/', buyer_profile, name='buyer_profile'),  # Buyer profile page
    path('artisan_profile/', artisan_profile, name='artisan_profile'),
    path('driver_profile/', driver_profile, name='driver_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('listed_products/', listed_products, name='listed_products'),  # Artisan's listed products
    path('order_history/', order_history, name='order_history'),
    path('products/<slug:slug>/', views.upcycled_product_details, name='upcycled_product_details'),
    path('upcycled_products/', views.upcycled_products, name='upcycled_products'),
    path('product/<int:pk>/edit/', views.edit_product,   name='edit_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('add-to-cart/<str:model_name>/<int:object_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('trash-items/', views.trash_item_list, name='trash_item_list'),
    path('trash/<slug:slug>/', views.trash_item_details, name='trash_item_details'),
    path('checkout/place_order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/fail/', views.payment_fail, name='payment_fail'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('payment/ipn/', views.payment_ipn, name='payment_ipn'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('driver/update-status/<int:order_id>/',views.update_delivery_status,name='update_delivery_status'),
    path('driver/update-expected/<int:order_id>/',views.update_expected_delivery,name='update_expected_delivery'),
    path('driver/delivery-history/', views.delivery_history, name='delivery_history'),
    path('orders/<int:order_id>/review/', views.write_review, name='write_review'),
    path('driver/reviews/', views.driver_reviews, name='driver_reviews'),
    path('search/', views.search_page, name='search_results'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)