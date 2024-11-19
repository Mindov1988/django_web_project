from django.http import JsonResponse
from django.views.generic import TemplateView, FormView

from electronics_shop.electronics.forms import ContactForm


class AboutInfoView(TemplateView):
    template_name = 'electronics/about.html'


class DeliveryInfoView(TemplateView):
    template_name = 'electronics/delivery_info.html'


class ContactInfoView(FormView):
    template_name = 'electronics/contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        print(f"Email: {email}, Message: {message}")

        return JsonResponse({"success": True, "message": "Thank you for your message!"})

    def form_invalid(self, form):
        return JsonResponse({"success": False, "errors": form.errors}, status=400)
