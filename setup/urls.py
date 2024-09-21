from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/transcricao/transcrever/', permanent=False)),
    path("conversor/", include("conversor.urls")),
    path("transcricao/", include("transcricao.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
