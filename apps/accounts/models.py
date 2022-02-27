from django.contrib.auth.models import User
from django.db import models

from apps.core.funcoes import sexo


class UserProfile(models.Model):

    SX_CHOICES = sexo.choices_sexo()

    photo = models.ImageField('Foto', upload_to='photos')
    cel_phone = models.CharField('Celular', max_length=16)

    data_nascimento = models.DateField(verbose_name='Data de Nascimento', null=True)
    sexo = models.CharField(max_length=1, choices=SX_CHOICES, default="", blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF", blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        db_table = 'UserProfile'
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos usuários'

    def __str__(self):
        return self.user.username
