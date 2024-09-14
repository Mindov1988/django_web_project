from django import forms
from electronics_shop.electronics.models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
