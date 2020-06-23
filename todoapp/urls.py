from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tarefas/', include('apps.tasks.urls', namespace='tasks')),
    path('contas/', include('apps.accounts.urls', namespace='accounts')),
    path('', include('core.urls', namespace='core')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
