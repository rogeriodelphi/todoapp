from django.contrib import admin
from django.utils.timezone import now

from apps.tasks.models import Category, Task, TaskMember


@admin.register(Category)
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
    list_display = (
        'id', 'title', 'user', 'start_time', 'end_time', 'list_categories', 'status', 'created_date', 'task_today')
    search_fields = ['title', 'description']
    date_hierarchy = 'start_time'
    list_filter = ['user', 'category', 'status']
    actions = [mark_all_tasks_done, mark_all_tasks_pending, mark_all_tasks_running]
    filter_horizontal = ['category']
    list_editable = ['title']

    def task_today(self, obj):
        return obj.start_time == now().date()
    task_today.short_description = 'Início hoje?'
    task_today.boolean = True


@admin.register(TaskMember)
class TaskMemberAdmin(admin.ModelAdmin):
    model = TaskMember
    list_display = ['task', 'user']
