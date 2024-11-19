from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(
        label='Your Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write your message here...',
            'rows': 5
        })
    )
