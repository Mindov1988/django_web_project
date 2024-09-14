from django.shortcuts import render, get_object_or_404
from electronics_shop.electronics.models import Order


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        'order': order
    }

    return render(request, 'orders/order_detail.html', context)
