from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include, re_path
from django.conf import settings
from electronics_shop.electronics.views import DeliveryInfoView, AboutInfoView, ContactInfoView, accept_cookies, \
    PrivacyInfoView


def custom_404_view(request, exception=None):
    if settings.DEBUG:
        return render(request, '404.html', status=404)
    return render(request, '404.html', status=404)


handler404 = 'electronics_shop.urls.custom_404_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('electronics_shop.common.urls')),
    path('categories/', include('electronics_shop.categories.urls')),
    path('products/', include('electronics_shop.products.urls')),
    path('wishlist/', include('electronics_shop.wishlist.urls')),
    path('cart/', include('electronics_shop.cart.urls')),
    path('checkout/', include('electronics_shop.checkout.urls')),
    path('order/', include('electronics_shop.orders.urls')),
    path('dashboard/', include('electronics_shop.dashboard.urls')),
    path('accounts/', include('electronics_shop.accounts.urls')),
    path('about/', AboutInfoView.as_view(), name='about'),
    path('contact/', ContactInfoView.as_view(), name='contact'),
    path('delivery/', DeliveryInfoView.as_view(), name='delivery_info'),
    path('accept-cookies/', accept_cookies, name='accept_cookies'),
    path('decline-cookies/', accept_cookies, name='decline_cookies'),
    path('privacy-policy/', PrivacyInfoView.as_view(), name='privacy_policy'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
