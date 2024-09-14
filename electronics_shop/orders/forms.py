from django import forms
from electronics_shop.electronics.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone_number']  # Add more fields as necessary

    full_name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
