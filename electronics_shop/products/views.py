from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Avg
from electronics_shop.electronics.models import Product
from electronics_shop.products.forms import ReviewForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    average_rating = product.reviews.aggregate(Avg('rating')).get('rating__avg') or 0

    reviews = product.reviews.all()
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]

    review_form = ReviewForm()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'review_form': review_form,
        'average_rating': average_rating,
    })

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

            return redirect('product_detail', pk=product.id)

    return render(request, 'products/add_review.html', {'review_form': ReviewForm, 'product': product})
