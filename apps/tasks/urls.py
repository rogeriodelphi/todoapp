from django.urls import path
from . import views

app_name = 'apps/tasks'

urlpatterns = [
    path('categorias/', views.list_categories, name='list_categories'),
    path('categorias/adicionar/', views.add_category, name='add_category'),
    path('categorias/editar/<int:id_category>/', views.edit_category, name='edit_category'),
    path('categorias/excluir/<int:id_category>/', views.delete_category, name='delete_category'),

    path('listar/', views.list_tasks, name='list_tasks'),
    path('adicionar/', views.add_task, name='add_task'),
    path('editar/<int:id_task>/', views.edit_task, name='edit_task'),
    path('excluir/<int:id_task>/', views.task_delete, name='task_delete'),

    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('task/<int:task_id>/details', views.task_details, name='task-detail'),
    path('add_taskmember/<int:task_id>', views.add_taskmember, name='add_taskmember'),
    path('task/<int:pk>/remove', views.TaskMemberDeleteView.as_view(), name='remove_task'),
]