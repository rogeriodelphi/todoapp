# Generated by Django 3.2.12 on 2022-02-27 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220226_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bairro',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Bairro'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='complemento',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Complemento'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='endereco',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Endereço'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='numero',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Número'),
        ),
    ]
