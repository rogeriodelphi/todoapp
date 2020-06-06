from django.contrib import admin

from apps.tasks.models import Category, Task


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'owner')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'end_date', 'priority', 'status', 'owner')



admin.site.register(Category, CategoryAdmin)
admin.site.register(Task, TaskAdmin)
