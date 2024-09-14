from asgiref.sync import sync_to_async
from django.urls import path
from electronics_shop.dashboard.views import dashboard_view

urlpatterns = (
    path('', dashboard_view, name='dashboard'),
)