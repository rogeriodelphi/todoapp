from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    photo = models.ImageField('Foto', upload_to='photos')
    cel_phone = models.CharField('Celular', max_length=16)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        db_table = 'UserProfile'
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos usuários'

    def __str__(self):
        return self.profile.user.username
