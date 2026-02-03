from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class FirstRunMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_exists = User.objects.filter(is_platform_admin=True).exists()
        setup_url_name = 'register' 
        setup_path = reverse(setup_url_name)

        if not admin_exists:
            # IMPORTANT: Allow access to the setup page itself to avoid infinite loop
            if request.path != setup_path and not request.path.startswith('/static/'):
                return redirect(setup_url_name)

        response = self.get_response(request)
        return response