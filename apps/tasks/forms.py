from django.forms.widgets import DateInput, Textarea
from apps.tasks.models import Task, Category, TaskMember
from django import forms

class CategoryForm(forms.ModelForm):
#    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Category
        exclude = ('user',)
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 3}),
        }

class TaskForm(forms.ModelForm):
#    end_time = forms.DateField(widget=DateInput(format='%d/%m/%Y'), input_formats=['%d/%m/%Y'])
#    end_time = forms.DateField(label='Data Final',
#    widget = DateInput(format='%d/%m/%Y', attrs={'maxlength': '10'}),
#        input_formats = ['%d/%m/%Y', ],)

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