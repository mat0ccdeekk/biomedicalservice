# Generated by Django 2.0 on 2021-01-15 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20210115_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquisti',
            name='ordinato',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Ordinato'),
        ),
    ]