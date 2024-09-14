from django.urls import path

from electronics_shop.wishlist.views import wishlist_view, add_to_wishlist, remove_from_wishlist, move_to_cart, \
    move_all_to_cart

urlpatterns = (
    path('', wishlist_view, name='wishlist_view'),
    path('add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('move_to_cart/<int:product_id>/', move_to_cart, name='move_to_cart'),
    path('move_all_to_cart/', move_all_to_cart, name='move_all_to_cart'),
)