# your_app/middleware/force_404_middleware.py

from django.conf import settings
from django.shortcuts import render


class Force404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # If the response status is 404, render the custom 404 page
        if response.status_code == 404 and settings.DEBUG:
            return render(request, '404.html', status=404)

        return response
