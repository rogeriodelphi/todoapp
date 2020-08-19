from django.forms.widgets import DateInput

from apps.tasks.models import Task, Category
from django import forms

class CategoryForm(forms.ModelForm):
#    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Category
        exclude = ('owner',)
    
class TaskForm(forms.ModelForm):
#    end_date = forms.DateField(widget=DateInput(format='%d/%m/%Y'), input_formats=['%d/%m/%Y'])
#    end_date = forms.DateField(label='Data Final',
#    widget = DateInput(format='%d/%m/%Y', attrs={'maxlength': '10'}),
#        input_formats = ['%d/%m/%Y', ],)
    class Meta:
        model = Task
        exclude = ('owner',)

