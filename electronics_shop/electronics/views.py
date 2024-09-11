# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, logger
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Product, Category, Order
from .forms import RegisterForm, LoginForm, ProductForm, ReviewForm, OrderForm
import logging


def index(request):
    return render(request, 'electronics/index.html')

class ProductListView(ListView):
    model = Product
    template_name = 'electronics/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'electronics/product_detail.html'
    context_object_name = 'product'

class CategoryListView(ListView):
    model = Category
    template_name = 'electronics/category_list.html'
    context_object_name = 'category_list'

class DashboardView(ListView):
    model = Order
    template_name = 'electronics/dashboard.html'

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to home page after successful registration
    else:
        form = RegisterForm()
    return render(request, 'electronics/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'electronics/login.html', {'form': LoginForm})

def logout_view(request):
    logout(request)  # Logs the user out
    messages.success(request, "You have been successfully logged out.")
    return redirect('index')

def about(request):
    return render(request, 'electronics/about.html')

def contact(request):
    return render(request, 'electronics/contact.html')

# class CategoryDetailView(DetailView):
#     model = Category
#     template_name = 'electronics/category_detail.html'
#     context_object_name = 'category'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Fetching all products that belong to this category
#         context['products'] = Product.objects.filter(category=self.object)
#         return context


def add_to_cart(request, product_id):
    # Fetch the product from the database
    product = get_object_or_404(Product, pk=product_id)

    # Get the quantity from the POST data, default to 1 if not provided or invalid
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1  # Default to 1 if there's an error in conversion

    # Cart logic: Store the cart in the session
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

    # Save the cart back to the session
    request.session['cart'] = cart

    # Provide feedback to the user
    messages.success(request, f'Added {quantity} {product.name}(s) to your cart.')

    # Redirect to the product detail page
    return redirect('product_detail', pk=product_id)

def cart_view(request):
    cart = request.session.get('cart', {})
    item_total_price = 0  # Initialize item_total_price

    if request.method == 'POST':
        if 'remove' in request.POST:
            product_id = request.POST.get('product_id')
            cart.pop(product_id, None)  # Remove the item from the cart
        elif 'edit' in request.POST:
            product_id = request.POST.get('product_id')
            new_quantity = int(request.POST.get('quantity'))
            if product_id in cart:
                cart[product_id]['quantity'] = new_quantity
                if new_quantity <= 0:
                    cart.pop(product_id)  # Remove the item if quantity is zero or less

        # Update the cart in the session
        request.session['cart'] = cart
        return redirect(reverse('cart_view'))  # Redirect to the cart view

    # Prepare cart items for display
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
        item_total_price = int(item['quantity']) * item['price']

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'item_total_price': item_total_price
    }

    return render(request, 'electronics/cart.html', context)



class CategoryDetailView(DetailView):
    model = Category
    template_name = 'electronics/category_detail.html'  # The template to show products in this category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category=self.object)  # Get products for this category
        return context

def checkout_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cart = request.session.get('cart', {})
            if not cart:
                messages.error(request, "Your cart is empty.")
                return redirect('cart_view')

            total_price = sum(item['price'] * item['quantity'] for item in cart.values())

            # Create a new order
            order = form.save(commit=False)
            order.total_price = total_price
            order.cart_data = cart
            order.user = request.user if request.user.is_authenticated else None
            order.save()

            # Clear the cart
            request.session['cart'] = {}

            messages.success(request, "Your order has been placed successfully.")
            return redirect('dashboard')
    else:
        form = OrderForm()

    return render(request, 'electronics/checkout.html', {'form': form})

def dashboard_view(request):
    # Filter orders by the logged-in user
    orders = Order.objects.filter(user=request.user) if request.user.is_authenticated else None

    context = {
        'orders': orders
    }

    return render(request, 'electronics/dashboard.html', context)


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        'order': order
    }

    return render(request, 'electronics/order_detail.html', context)


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()

            # Redirect back to the product detail page
            return redirect('product_detail', pk=product.id)
    else:
        form = ReviewForm()

    return render(request, 'electronics/add_review.html', {'review_form': ReviewForm, 'product': product})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Calculate average rating
    average_rating = product.reviews.aggregate(Avg('rating')).get('rating__avg') or 0

    reviews = product.reviews.all()
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]

    review_form = ReviewForm()

    return render(request, 'electronics/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'review_form': review_form,
        'average_rating': average_rating,  # Pass the average rating to the template
    })


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)  # Convert to string to match keys in cart

        if product_id_str in cart:
            del cart[product_id_str]
            request.session['cart'] = cart
            request.session.modified = True  # Ensure session is saved
        else:
            print(f"Product ID {product_id_str} not found in cart.")

        return redirect('cart_view')
    else:
        return redirect('cart_view')