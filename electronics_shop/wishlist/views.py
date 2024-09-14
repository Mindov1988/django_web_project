from django.shortcuts import render, redirect
from electronics_shop.electronics.models import Product


def wishlist_view(request):
    wishlist = request.session.get('wishlist', {})

    wishlist_items = []
    for product_id, item in wishlist.items():
        wishlist_items.append({
            'product_id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image_url': item['image_url'],
            'total_price': item['price'] * item['quantity']
        })

    context = {
        'wishlist_items': wishlist_items,
    }

    return render(request, 'wishlist/wishlist.html', context)


def add_to_wishlist(request, product_id):
    product = Product.objects.get(pk=product_id)

    wishlist = request.session.get('wishlist', {})

    if str(product_id) not in wishlist:
        wishlist[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image_url': product.image.url
        }
    else:
        wishlist[str(product_id)]['quantity'] += 1

    request.session['wishlist'] = wishlist
    request.session.modified = True

    return redirect('wishlist_view')


def remove_from_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', {})
    product_id_str = str(product_id)

    if product_id_str in wishlist:
        del wishlist[product_id_str]
        request.session['wishlist'] = wishlist
        request.session.modified = True

    return redirect('wishlist_view')


def move_to_cart(request, product_id):
    wishlist = request.session.get('wishlist', {})
    cart = request.session.get('cart', {})

    product_id_str = str(product_id)
    if product_id_str in wishlist:
        cart[product_id_str] = wishlist[product_id_str]
        del wishlist[product_id_str]

        request.session['cart'] = cart
        request.session['wishlist'] = wishlist
        request.session.modified = True

    return redirect('cart_view')


def move_all_to_cart(request):
    wishlist = request.session.get('wishlist', {})
    cart = request.session.get('cart', {})

    for product_id, item in wishlist.items():
        cart[product_id] = {
            'name': item['name'],
            'price': float(item['price']),
            'quantity': item['quantity'],
            'image_url': item['image_url']
        }

    request.session['cart'] = cart
    request.session['wishlist'] = {}
    request.session.modified = True

    return redirect('cart_view')
