from django.urls import path
from electronics_shop.categories.views import CategoryDetailView, CategoryListView

urlpatterns = (
    path('', CategoryListView.as_view(), name='category_list'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
)