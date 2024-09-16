from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from electronics_shop.electronics.models import Product
from electronics_shop.orders.forms import OrderForm


def checkout_view(request):
    # Check if the request is for direct checkout of a product
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Direct Checkout (for a single product)
            if product_id:
                product = get_object_or_404(Product, pk=product_id)
                total_price = product.price * quantity

                # Create the order with the product data
                order = form.save(commit=False)
                order.total_price = total_price
                order.cart_data = {
                    product_id: {
                        'name': product.name,
                        'price': product.price,
                        'quantity': quantity,
                    }
                }
                order.user = request.user if request.user.is_authenticated else None
                order.save()

                messages.success(request, "Your order for {} has been placed successfully.".format(product.name))
                return redirect('dashboard')

            # Regular Cart Checkout
            else:
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

                # Clear the cart after the order is placed
                request.session['cart'] = {}

                messages.success(request, "Your order has been placed successfully.")
                return redirect('dashboard')
    else:
        form = OrderForm()

    return render(request, 'checkout/checkout.html', {'form': form})
