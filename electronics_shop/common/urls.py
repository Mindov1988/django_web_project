from django.urls import path
from electronics_shop.common.views import index

urlpatterns = (
    path('', index, name='index'),
)