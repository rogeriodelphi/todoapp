import base64
from django.forms import fields, widgets
from django.forms.models import ModelMultipleChoiceField

from apps.core import choices
from apps.core import formwidgets
from apps.core.utils import ChainedModelMultipleChoiceField


class TransferSelectField(ModelMultipleChoiceField):
    widget = formwidgets.TransferSelectWidget


class ChainedTransferSelectField(ChainedModelMultipleChoiceField):
    widget = formwidgets.ChainedTransferSelectWidget


class PhotoCaptureField(fields.Field):
    widget = formwidgets.PhotoCaptureInput

    def to_python(self, value):
        if value:
            return base64.b64decode(value.split(',')[1])
        else:
            return None


class YesNoChoiceField(fields.TypedChoiceField):
    """
    Deve ser usado em fomulários quando precisar de um campo que
    exiba botões de seleção do tipo rádio e tenha o seu valor como booleano.
    Pode usar em ModelForm onde o campo correspondente no modelo é um
    BooleanField.
    Ao passar o argumento empty_label=True será gerada uma opção vazia com
    valor = "" e label = "------". Para personalizar este label, passe uma
    string ao invés de um booleano.
    """
    widget = widgets.RadioSelect

    def __init__(self, empty_label=None, **kwargs):
        if "coerce" not in kwargs:
            kwargs["coerce"] = lambda x: x == "1"
        choices_ = kwargs.get("choices", choices.YesNo.choices)
        if empty_label is not None:
            if empty_label is True:
                empty_label = "---------"
            empty_value = kwargs.get("empty_value", "")
            empty_choice = [(empty_value, empty_label),]
            choices_ = empty_choice + choices_
        kwargs["choices"] = choices_
        super().__init__(**kwargs)


class BloodPressureField(fields.MultiValueField):
    widget = formwidgets.BloodPressure

    def __init__(self, **kwargs):
        fields_ = (
            fields.IntegerField(min_value=0, max_value=300),
            fields.IntegerField(min_value=0, max_value=300)
         )
        super().__init__(fields=fields_, **kwargs)

    def compress(self, data_list):
        return "x".join(map(str, data_list))


class NumberScaleField(fields.ChoiceField):
    widget = formwidgets.NumberScaleRadio
    use_label_as_title = True

    def __init__(self, choices=(), use_value_as_label=True, use_label_as_title=True, **kwargs):
        self.use_label_as_title = use_label_as_title
        if use_value_as_label:
            choices = (
                (key, key)
                for key, value in choices
            )
        super().__init__(choices=choices, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None
        return value
