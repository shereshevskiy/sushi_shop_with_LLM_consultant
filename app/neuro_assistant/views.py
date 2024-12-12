from django.shortcuts import render


def dialog(request):
    return render(request, 'dialog.html')