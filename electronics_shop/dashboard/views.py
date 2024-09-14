from django.shortcuts import render
from electronics_shop.electronics.models import Order


def dashboard_view(request):
    orders = Order.objects.filter(user=request.user) if request.user.is_authenticated else None

    context = {
        'orders': orders
    }

    return render(request, 'dashboard/dashboard.html', context)
