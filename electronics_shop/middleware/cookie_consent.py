class CookieConsentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.COOKIES.get('cookies_accepted') == 'false':
            response.delete_cookie('show_cookie_banner')
        elif not request.COOKIES.get('cookies_accepted'):
            response.set_cookie('show_cookie_banner', 'true', max_age=3600)

        return response
