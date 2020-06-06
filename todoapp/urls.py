from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tarefas/', include('apps.tasks.urls', namespace='tasks')),
    path('', include('core.urls', namespace='core')),
]
