from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('categoria/', include('apps.tasks.urls', namespace='category')),
    path('', include('core.urls', namespace='core')),
]
