from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from electronics_shop.electronics.models import Product


def cart_view(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        cart_items.append({
            'product_id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image_url': item['image_url'],
            'total_price': item['price'] * item['quantity']
        })
        total_price += item['price'] * item['quantity']

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'image_url': product.image.url
        }

    request.session['cart'] = cart

    messages.success(request, f'Added {quantity} {product.name}(s) to your cart.')

    return redirect('product_detail', pk=product_id)


def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)

        if product_id_str in cart:
            cart[product_id_str]['quantity'] = quantity
            request.session['cart'] = cart
            request.session.modified = True
        else:
            print(f"Product ID {product_id_str} not found in cart.")

        return redirect('cart_view')
    else:
        return redirect('cart_view')


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)

        if product_id_str in cart:
            del cart[product_id_str]
            request.session['cart'] = cart
            request.session.modified = True
        else:
            print(f"Product ID {product_id_str} not found in cart.")

        return redirect('cart_view')
    else:
        return redirect('cart_view')



