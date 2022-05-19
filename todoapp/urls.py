from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('apps.accounts.urls', namespace='accounts')),
    path('', include('apps.core.urls', namespace='core')),
    path('', include('apps.tasks.urls', namespace='tasks')),
    path('oauth/', include('social_django.urls', namespace='social'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
