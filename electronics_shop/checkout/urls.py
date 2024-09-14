from django.urls import path

from electronics_shop.checkout.views import checkout_view

urlpatterns = (
    path('', checkout_view, name='checkout'),
)