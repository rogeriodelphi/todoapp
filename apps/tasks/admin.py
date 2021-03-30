from django.contrib import admin

from apps.tasks.models import Category, Task


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'user')
    search_fields = ['title', 'description']
    list_filter = ['user']

def mark_all_tasks_done(modeladmin, request, queryset):
    queryset.update(status='AF')
mark_all_tasks_done.short_description = "Marcar como 'A Fazer' todas as tarefas"

def mark_all_tasks_pending(modeladmin, request, queryset):
    queryset.update(status='FA')
mark_all_tasks_pending.short_description = "Marcar como 'Fazendo' todas as tarefas"

def mark_all_tasks_running(modeladmin, request, queryset):
    queryset.update(status='CO')
mark_all_tasks_running.short_description = "Marcar como 'Concluída' todas as tarefas"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'start_time','end_time', 'priority', 'list_categories', 'status', 'created_date')
    search_fields = ['title', 'description']
    list_filter = ['priority', 'user', 'category', 'status']
    actions = [mark_all_tasks_done, mark_all_tasks_pending, mark_all_tasks_running]

#    def list_categories(self, obj):
#        return ", ".join([c.name for c in obj.category.all()])
#    list_categories.short_description = "Categorias"


admin.site.register(Category, CategoryAdmin)
#admin.site.register(Task, TaskAdmin)
