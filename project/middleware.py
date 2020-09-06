# from django.conf import settings
# import re
# from django.shortcuts import redirect

# EXEMPT_URLS = [re.compile(settings.LOGIN_URL)]
# if hasattr(settings,'LOGIN_EXEMPT_URLS'):
#     EXEMPT_URLS = [settings.LOGIN_EXEMPT_URLS]

# class LoginRequiredMiddleware:
#     def __init__(self,get_response):
#         self.get_response = get_response

#     def __call__(self,request):
#         response = self.get_response(request)
#         return response

#     def process_view(self,request, view_func, view_args, view_kwargs):
#         assert hasattr(request, 'user')
#         path = request.path_info
#         print(path)

#         if not request.user.is_authenticated:
#             for url in EXEMPT_URLS:
#                 if not path == url:
#                     return redirect('/')
