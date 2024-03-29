# Generated by Django 2.2.5 on 2021-03-30 04:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Nome')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'Category',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título da Tarefa')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('start_time', models.DateField(verbose_name='Data Inicial')),
                ('end_time', models.DateField(verbose_name='Data Final')),
                ('priority', models.CharField(choices=[('B', 'Baixa'), ('M', 'Média'), ('A', 'Alta')], max_length=1, verbose_name='Prioridade')),
                ('status', models.CharField(choices=[('AF', 'A fazer'), ('FA', 'Fazendo'), ('CO', 'Concluída')], max_length=2, verbose_name='Status')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ManyToManyField(to='tasks.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tarefa',
                'verbose_name_plural': 'Tarefas',
                'db_table': 'Task',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TaskMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('task', 'user')},
            },
        ),
    ]
