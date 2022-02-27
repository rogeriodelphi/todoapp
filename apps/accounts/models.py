from django.contrib.auth.models import User
from django.db import models

from apps.core.funcoes import sexo, estados


class UserProfile(models.Model):

    SX_CHOICES = sexo.choices_sexo()
    UF_CHOICES = estados.choices_estados()

    photo = models.ImageField('Foto', upload_to='photos')

    data_nascimento = models.DateField(verbose_name='Data de Nascimento', null=True)
    sexo = models.CharField(max_length=1, choices=SX_CHOICES, default="", blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF", blank=True, null=True)

    endereco = models.CharField(max_length=50, verbose_name="Endereço", blank=True, null=True)
    numero = models.CharField(max_length=6, verbose_name="Número", blank=True, null=True)
    complemento = models.CharField(max_length=60, verbose_name="Complemento", null=True, blank=True)
    bairro = models.CharField(max_length=50, verbose_name="Bairro", null=True, blank=True)

    cidade = models.CharField(max_length=30, verbose_name="Cidade", null=True, blank=True)
    estado = models.CharField(max_length=2, choices=UF_CHOICES, default="BA", verbose_name="Estado")
    cep = models.CharField(max_length=9, verbose_name="CEP", null=True, blank=True)
    cel_phone = models.CharField('Celular', max_length=16)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        db_table = 'UserProfile'
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos usuários'

    def __str__(self):
        return self.user.username
