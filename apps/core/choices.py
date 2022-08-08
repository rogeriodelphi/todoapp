from django.db.models import IntegerChoices


class YesNo(IntegerChoices):
    YES = 1, "Sim"
    NO = 0, "Não"

