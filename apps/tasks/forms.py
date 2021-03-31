from django import forms
from django.forms.widgets import Textarea

from apps.tasks.models import Category, Task, TaskMember


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('user',)
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 3}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['user']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 3}),
        }


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = TaskMember
        fields = ['user']
