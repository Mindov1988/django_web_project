from django.shortcuts import render, redirect
from django.contrib import messages
from electronics_shop.orders.forms import OrderForm


def checkout_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cart = request.session.get('cart', {})
            if not cart:
                messages.error(request, "Your cart is empty.")
                return redirect('cart_view')

            total_price = sum(item['price'] * item['quantity'] for item in cart.values())

            order = form.save(commit=False)
            order.total_price = total_price
            order.cart_data = cart
            order.user = request.user if request.user.is_authenticated else None
            order.save()

            request.session['cart'] = {}

            messages.success(request, "Your order has been placed successfully.")
            return redirect('dashboard')
    else:
        form = OrderForm()

    return render(request, 'checkout/checkout.html', {'form': form})
