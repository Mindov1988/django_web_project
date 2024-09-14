from django.shortcuts import render
from django.views.generic import TemplateView


class AboutInfoView(TemplateView):
    template_name = 'electronics/about.html'

class ContactInfoView(TemplateView):
    template_name = 'electronics/contact.html'


class DeliveryInfoView(TemplateView):
    template_name = 'electronics/delivery_info.html'