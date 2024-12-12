from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('dialog/', views.dialog, name='dialog'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT / 'neuro_assistant' )