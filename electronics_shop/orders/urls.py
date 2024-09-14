from django.urls import path

from electronics_shop.orders.views import order_detail_view

urlpatterns = (
path('<int:order_id>/', order_detail_view, name='order_detail'),
)