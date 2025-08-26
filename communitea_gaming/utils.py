from django.http import JsonResponse

def is_admin(request):
    is_admin = request.user.is_authenticated and request.user.is_staff
    return JsonResponse({ "is_admin": is_admin })