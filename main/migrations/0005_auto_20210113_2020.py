# Generated by Django 2.0 on 2021-01-13 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210113_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquisti',
            name='creato',
            field=models.DateField(verbose_name='Data acquisto'),
        ),
    ]