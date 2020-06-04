from apps.tasks.models import Task, Category
from django import forms

class CategoryForm(forms.ModelForm):
#    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Category
        exclude = ('owner',)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('owner',)