from django.conf import settings
from django.shortcuts import render


def dialog(request):
    context = {
        'consultant_api_url': settings.CONSULTANT_API_URL
    }
    return render(request, 'dialog.html', context)
