# Generated by Django 2.0 on 2021-01-15 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_acquisti_prezzo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquisti',
            name='autore',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='acquisti',
            name='prezzo',
            field=models.IntegerField(default='0', verbose_name='importo'),
        ),
    ]