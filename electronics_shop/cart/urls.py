from django.urls import path
from electronics_shop.cart.views import cart_view, add_to_cart, update_cart, remove_from_cart

urlpatterns = (
    path('', cart_view, name='cart_view'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update/<int:product_id>/', update_cart, name='cart_update'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
)