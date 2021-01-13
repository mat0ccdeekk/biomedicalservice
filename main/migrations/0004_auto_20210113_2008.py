# Generated by Django 2.0 on 2021-01-13 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210113_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='acquisti',
            name='descrizione',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='acquisti',
            name='quantita',
            field=models.IntegerField(blank=True, default='1', verbose_name='quantità'),
        ),
        migrations.AddField(
            model_name='dispositivo',
            name='prezzo',
            field=models.IntegerField(default='0'),
        ),
    ]