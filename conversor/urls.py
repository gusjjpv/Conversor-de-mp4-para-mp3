from django.urls import path
from .views import ConverterView

urlpatterns = [
    path("", ConverterView.as_view(), name="home"),
]
