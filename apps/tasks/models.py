from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField('Nome', max_length=150)
    description = models.TextField('Descrição', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Category'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

    def __str__(self):
        return self.title

class Priority(models.Model):
    description = models.CharField('Descrição', max_length=100)
    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.description

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('B', 'Baixa'),
        ('M', 'Média'),
        ('A', 'Alta'),
    )

    STATUS_CHOICES = (
        ('AF', 'A fazer'),
        ('FA', 'Fazendo'),
        ('CO', 'Concluída'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Título da Tarefa', max_length=200)
    description = models.TextField('Descrição')
    start_time = models.DateField('Data Inicial')
    end_time = models.DateField('Data Final')
    # priority = models.ManyToManyField(Priority, verbose_name="Priority", related_name="priorities", blank=True)
    priority = models.CharField('Prioridade', max_length=1, choices=PRIORITY_CHOICES)
    category = models.ManyToManyField(Category)
    status = models.CharField('Status', max_length=2, choices=STATUS_CHOICES)
    created_date = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        db_table = 'Task'
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering = ['-start_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks:task-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('tasks:task-detail', args=(self.id,))
        print(url)
        return f'<a href="{url}"> {self.title} </a>'

    def __str__(self):
        return self.title

    def list_categories(self):
        return ", ".join([c.title for c in self.category.all()])

    list_categories.short_description = "Categorias"


class TaskMember(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['task', 'user']

    def __str__(self):
        return str(self.user)



