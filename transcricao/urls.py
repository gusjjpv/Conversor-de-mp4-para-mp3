from django.urls import path
from .views import TranscribeView

urlpatterns = [
    path('transcrever/', TranscribeView.as_view(), name='transcrever'),
]
