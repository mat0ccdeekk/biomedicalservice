# Generated by Django 2.0 on 2021-01-15 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210115_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquisti',
            name='prezzo',
            field=models.IntegerField(blank=True, default='0', null=True, verbose_name='importo'),
        ),
    ]
