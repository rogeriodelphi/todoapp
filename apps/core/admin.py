from django.contrib import admin

from django.contrib.auth.models import User, Group

#admin.site.unregister(User)
#admin.site.unregister(Group)


admin.site.site_header = "ToDoApp Login"
admin.site.title = "Administração ToDoApp"
admin.site.index_title = "Administração - Aplicações"
