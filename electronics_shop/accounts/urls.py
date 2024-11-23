from django.urls import path
from electronics_shop.accounts.views import register, login_view, logout_view, DetailsProfileView, EditProfileView, \
    DeleteProfileView

urlpatterns = (
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('details/', DetailsProfileView.as_view(), name='details profile'),
    path('edit/', EditProfileView.as_view(), name='edit profile'),
    path('delete/', DeleteProfileView.as_view(), name='delete profile'),
)
