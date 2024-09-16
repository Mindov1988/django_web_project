from django.urls import path

from electronics_shop import checkout
from electronics_shop.products.views import ProductDetailView, add_review


urlpatterns = (
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:product_id>/review/', add_review, name='add_review'),
)