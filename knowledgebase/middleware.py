from django.utils.deprecation import MiddlewareMixin

class LimitedModeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        mode = request.GET.get('mode')
        if mode == 'readonly':
            request.session['limited_mode'] = True
        elif mode == 'full':
            request.session['limited_mode'] = False
        request.limited_mode = bool(request.session.get('limited_mode', False))
