from unittest.mock import patch

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from electronics_shop.electronics.views import ProductListView, ProductDetailView, CategoryListView, DashboardView, \
    register, login_view, logout_view, about, contact, add_to_cart, index, CategoryDetailView, cart_view, \
    dashboard_view, checkout_view, order_detail_view, add_review, remove_from_cart, update_cart, wishlist_view, \
    add_to_wishlist, remove_from_wishlist, move_to_cart, move_all_to_cart, DeliveryInfoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
path('product/<int:product_id>/review/', add_review, name='add_review'),
    path('categories/', CategoryListView.as_view(), name='category_list'),  # URL for listing all categories
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),  # URL for category detail view
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', update_cart, name='cart_update'),
    path('cart/checkout/', checkout_view, name='checkout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('order/<int:order_id>/', order_detail_view, name='order_detail'),
    path('wishlist/', wishlist_view, name='wishlist_view'),
path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/move_to_cart/<int:product_id>/', move_to_cart, name='move_to_cart'),
    path('wishlist/move_all_to_cart/', move_all_to_cart, name='move_all_to_cart'),
    path('delivery/', DeliveryInfoView.as_view(), name='delivery_info'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)