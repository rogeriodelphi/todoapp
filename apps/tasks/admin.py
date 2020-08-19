from django.contrib import admin

from apps.tasks.models import Category, Task


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'owner')
    search_fields = ['name', 'description']
    list_filter = ['owner']

def mark_all_tasks_done(modeladmin, request, queryset):
    queryset.update(status='CD')
mark_all_tasks_done.short_description = "Marcar como 'concluída' todas as tarefas"

def mark_all_tasks_pending(modeladmin, request, queryset):
    queryset.update(status='PD')
mark_all_tasks_pending.short_description = "Marcar como 'Pendente' todas as tarefas"

def mark_all_tasks_running(modeladmin, request, queryset):
    queryset.update(status='EX')
mark_all_tasks_running.short_description = "Marcar como 'Em execução' todas as tarefas"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'end_date', 'priority', 'list_categories', 'status')
    search_fields = ['name', 'description']
    list_filter = ['priority', 'owner', 'category', 'status']
    actions = [mark_all_tasks_done, mark_all_tasks_pending, mark_all_tasks_running]

#    def list_categories(self, obj):
#        return ", ".join([c.name for c in obj.category.all()])
#    list_categories.short_description = "Categorias"


admin.site.register(Category, CategoryAdmin)
#admin.site.register(Task, TaskAdmin)
