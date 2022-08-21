from django import forms
from django.forms.widgets import Textarea



from django.db.transaction import atomic
from django.utils import timezone
from django.utils.formats import localize
from djangoformsetjs.utils import formset_media_js

from apps.core.formfields import YesNoChoiceField, BloodPressureField, NumberScaleField
from apps.core.formwidgets import Cid10ModelSelect2Widget, NotApplicableCheckboxInput, \
    Cid10ModelSelect2MultipleWidget, NotApplicableRadioSelect, NumberScaleRadio, \
    RadioSelectClearable, DateTimeWidget, BloodPressure, CuidadoModelSelect2MultipleWidget
# # from apps.core.utils import add_attrs_for_fields, today, remove_empty_option_in_radio_select
# from apps.core.utils import meu_vinculo

from apps.core import models, choices
# from django_select2.forms import ModelSelect2Widget, Select2Widget, ModelSelect2MultipleWidget

# from apps.core.utils import CpfFormField




from apps.tasks.models import Category, Task, TaskMember

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('user',)
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 3}),
        }


class TaskForm(forms.ModelForm):
    # fieldsets = {
    #     'titulo': {
    #         'fields': [
    #             'title',
    #             'description',
    #         ]
    #     },
    #     'dados': {
    #         'fields': [
    #             'start_time',
    #             'end_time',
    #             'priority',
    #             'category',
    #             'status',
    #         ]
    #     },
    # }
    # options = {
    #     # Título
    #     'title': {"grid": '6'},
    #     'description': {"grid": '6'},
    #
    #
    #     # Dados
    #     'start_time': {"grid": '12'},
    #     'end_time': {"grid": '12'},
    #     'priority': {"grid": '6'},
    #     'category': {"grid": '6'},
    # }

    class Meta:
        model = Task
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 3}),
        }
        fields = (
            'title',
            'description',
            'start_time',
            'end_time',
            'priority',
            'category',
            'status',
        )
        exclude = ['user']


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = TaskMember
        fields = ['user']
